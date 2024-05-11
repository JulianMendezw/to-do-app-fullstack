// Hooks
import { useState } from 'react';

// Styles
import './style.scss'

// Icons
import { MdRadioButtonUnchecked } from "react-icons/md";
import { TbCircleCheckFilled } from "react-icons/tb";
import { TiTimes } from "react-icons/ti";
import { TiPlus } from "react-icons/ti";
import { MdOutlineLogin } from "react-icons/md";


type Todo = {
    id: number;
    text: string;
    completed: boolean;
};

const defaultTask = [{
    id: 1,
    text: "New feature dark mode",
    completed: false,
},
{
    id: 2,
    text: "Deploy Frontend",
    completed: true,
},
{
    id: 3,
    text: "Integration to master",
    completed: false,
},
]

export const ToDoList: React.FC = () => {

    // State to store task list
    const [tasks, setTask] = useState<Todo[]>(defaultTask);

    // State to store the new task
    const [newTask, setNewTask] = useState<string>('');

    // Function to handle the value of a new task
    const handleInputChange = (value: string) => {
        setNewTask(value);
    };

    // Function to add a task to the list
    const handleSubmit = (event: any) => {
        event.preventDefault();
        if (newTask.trim() !== '') {
            const newId = tasks.length > 0 ? tasks[tasks.length - 1].id + 1 : 1;
            // Add new task to the list
            setTask([...tasks, { id: newId, text: newTask.trim(), completed: false }]);
            // Clear input of the new task
            setNewTask('');
        }
    };

    // Function to mark a task as complete
    const handleComplete = (id: number) => {
        setTask(
            tasks.map((task) =>
                task.id === id ? { ...task, completed: !task.completed } : task
            )
        );
    };

    // Function to deleted a task from the list
    const handleDelete = (id: number) => {
        setTask(tasks.filter((task) => task.id !== id));
    };

    // Function to log out
    const logOut = () => {
        localStorage.setItem("Authorization", "false")
        window.location.reload();
    }

    return (

        <div className='to-app-list'>
            <div className="header-section">
                <h1>Tasks</h1>
                <button className='logout' type='button' onClick={() => logOut()}><MdOutlineLogin /></button>
            </div>
            <form onSubmit={(event: any) => handleSubmit(event)}>

                {/* add new task  section */}
                <div className="add-section">
                    <input
                        type="text"
                        value={newTask}
                        onChange={(event: React.ChangeEvent<HTMLInputElement>) => handleInputChange(event.target.value)}
                        placeholder="New task..."
                        className='add-text'
                    />
                    <button className='add-task' type="submit"><TiPlus /></button>
                </div>
            </form>

            {/* task list */}
            {tasks.length >= 1 && <ul className='task-list'>
                {tasks.map((task, index) => (
                    <li className='task-element' key={index}>
                        <p>{task.text}</p>
                        <button className='check-button' onClick={() => handleComplete(task.id)}>
                            {task.completed ? <TbCircleCheckFilled /> : <MdRadioButtonUnchecked />}
                        </button>
                        <button className='delete-button' onClick={() => handleDelete(task.id)}><TiTimes /></button>
                    </li>
                ))}
            </ul>}
        </div>
    )
}

export default ToDoList;