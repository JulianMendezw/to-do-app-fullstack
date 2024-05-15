import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:8000';

export const GetTask = async (token: any) => {
  try {

    const headers = {
      'Authorization': 'Bearer ' + token,
      'accept': 'application/json',
    }

    const response = await axios.get(BASE_URL + '/tasks', { headers });
    return response.data;
  } catch (error) {
    console.error('Error fetching tasks:', error);
    return null;
  }
}

export const CreateTask = async (token: any, taskData: any) => {
  try {

    console.log(taskData)

    const headers = {
      'Authorization': 'Bearer ' + token,
      'accept': 'application/json',
    }
    const response = await axios.post(BASE_URL + '/create_task', taskData, { headers });
    return response.data;
  } catch (error) {
    console.error('Error fetching tasks:', error);
    return null;
  }
}


export const deleteTask = async (task_id: number) => {
  try {
    const headers = { "Content-Type": "application/x-www-form-urlencoded" };
    const response = await axios.delete(`${BASE_URL}/tasks/${task_id}`, { headers });
    return response.data;
  } catch (error) {
    console.error('Error deleting task:', error);
    return null;
  }
}
