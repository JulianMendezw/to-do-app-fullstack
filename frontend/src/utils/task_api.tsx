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


export const DeleteTask = async (token: any, task_id: number) => {
  try {
    const headers = {
      'Authorization': 'Bearer ' + token,
      'accept': 'application/json',
    }

    const response = await axios.delete(`${BASE_URL}/delete_task/${task_id}`, { headers });
    return response.data;
  } catch (error) {
    console.error('Error deleting task:', error);
    return null;
  }
}


export const UpdateTask = async (token: any, task_id: number, completed: boolean = true) => {

  try {
    const myHeaders = new Headers();
    myHeaders.append("accept", "application/json");
    myHeaders.append("Authorization", "Bearer " + token);

    const requestOptions: any = {
      method: "PUT",
      headers: myHeaders,
      redirect: "follow"
    };

    fetch(`${BASE_URL}/update_task/${task_id}?completed=${completed}`, requestOptions)
      .then((response) => response.text())
      .then((result) => console.log(result))
      .catch((error) => console.error(error));
  } catch (error) {
    console.error('Error updating task:', error);
    return null;
  }
}
