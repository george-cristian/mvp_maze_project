from django.contrib.auth.models import User
from .models import Maze
from knox.models import AuthToken
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status

class MazeTestCase(APITestCase):
    """
    Test suite for Maze
    """

    def setUp(self):
        """Set up the test suite"""
        self.first_user = User.objects.create_user(
            username="testuser1",
            password="test_password1"
        )
        self.second_user = User.objects.create_user(
            username="testuser2",
            password="test_password2"
        )

        _, self.token = AuthToken.objects.create(self.first_user)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        self.first_maze = Maze.objects.create(owner=self.first_user, gridSize="4x4", entrance="A1", walls=["A2", "C2", "A3", "A4", "C4", "D4"])
        self.multiple_exits_maze = Maze.objects.create(owner=self.first_user, gridSize="4x4", entrance="A1", walls=["A2", "C2", "A3", "A4", "D4"])
        self.no_exit_maze = Maze.objects.create(owner=self.first_user, gridSize="4x4", entrance="A1", walls=["C1", "A2", "C2", "B3", "C3"])

        self.second_maze = Maze.objects.create(owner=self.second_user, gridSize="9x9", entrance="B1", walls=["D2", "E2"])

        self.mazes = Maze.objects.all()

    def test_create_maze_invalid_grid_size(self):
        """Test the creation of one maze when the grid size format is invalid"""
        # arrange
        data = {"gridSize": "x9", "entrance": "A1", "walls": ["B1", "C1"]}

        # act
        response = self.client.post('/maze/', data)

        # assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_maze_zero_grid_size(self):
        """Test the creation of one maze when the grid size contains a zero"""
        # arrange
        data = {"gridSize": "0x9", "entrance": "A1", "walls": ["B1", "C1"]}

        # act
        response = self.client.post('/maze/', data)

        # assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_maze_invalid_entrance(self):
        """Test the creation of one maze when the entrance format is invalid"""
        # arrange
        data = {"gridSize": "9x9", "entrance": "1A", "walls": ["B1", "C1"]}

        # act
        response = self.client.post('/maze/', data)

        # assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_maze_invalid_wall(self):
        """Test the creation of one maze when the format of one of the walls is invalid"""
        # arrange
        data = {"gridSize": "9x9", "entrance": "A1", "walls": ["B0", "C1"]}

        # act
        response = self.client.post('/maze/', data)

        # assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_maze_wall_out_of_bounds(self):
        """Test the creation of one maze when one of the walls is out of bounds"""
        # arrange
        data = {"gridSize": "9x9", "entrance": "A1", "walls": ["B10", "C1"]}

        # act
        response = self.client.post('/maze/', data)

        # assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_maze_walls_on_bottom_edge(self):
        """Test the creation of one maze when the bottom edge of the maze contains walls"""
        # arrange
        data = {"gridSize": "2x2", "entrance": "A1", "walls": ["A2", "B2"]}

        # act
        response = self.client.post('/maze/', data)

        # assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_mazes(self):
        """Test the MazeViewSet maze get function"""
        # arrange -> done by setUp

        # act
        response = self.client.get('/maze/')

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['data']), 3)
        self.assertEqual(response.json()['data'][0]['id'], str(self.first_maze.id))
        self.assertEqual(response.json()['data'][1]['id'], str(self.multiple_exits_maze.id))
        self.assertEqual(response.json()['data'][2]['id'], str(self.no_exit_maze.id))

    def test_get_one_specific_maze(self):
        """Test the retrieval of one specific maze"""
        # arrange

        # act
        response = self.client.get(f'/maze/{self.first_maze.id}/')

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['data']['id'], str(self.first_maze.id))

    def test_get_one_specific_maze_not_owned(self):
        """Test the retrieval of one specific maze when that maze does not belong to the current user"""
        # arrange

        # act
        response = self.client.get(f'/maze/{self.second_maze.id}/')

        # assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_solution_no_query_params(self):
        """Test the solution endpoint when no query params are provided"""
        # arrange

        # act
        response = self.client.get(f'/maze/{self.first_maze.id}/solution/')

        # assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_solution_invalid_query_params(self):
        """Test the solution endpoint when invalid query params are provided"""
        # arrange

        # act
        response = self.client.get(f'/maze/{self.first_maze.id}/solution/?steps=medium')

        # assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_solution_min_good_weather(self):
        """Test the solution endpoint for the shortest path under good weather"""
        # arrange

        # act
        response = self.client.get(f'/maze/{self.first_maze.id}/solution/?steps=min')
        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['path'], ["A1", "B1", "B2", "B3", "B4"])

    def test_get_solution_max_good_weather(self):
        """Test the solution endpoint for the longest path under good weather"""
        # arrange

        # act
        response = self.client.get(f'/maze/{self.first_maze.id}/solution/?steps=max')
        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['path'], ["A1", "B1", "C1", "D1", "D2", "D3", "C3", "B3", "B4"])

    def test_get_solution_multiple_exits_found(self):
        """Test the solution endpoint when there are multiple exits in the maze"""
        # arrange

        # act
        response = self.client.get(f'/maze/{self.multiple_exits_maze.id}/solution/?steps=min')
        # assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_solution_no_exit(self):
        """Test the solution endpoint when there is no possible exit from the maze"""
        # arrange

        # act
        response = self.client.get(f'/maze/{self.no_exit_maze.id}/solution/?steps=min')
        # assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
