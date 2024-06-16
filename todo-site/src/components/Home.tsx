import React, { useEffect } from "react";
import Navbar from "./Navbar"
import Task from "../Common/task"

const todoApi: string = "https://qyhn475cesi4fkcbvysiy6446u0imidk.lambda-url.us-east-1.on.aws";
const userId: string = "1414";

function Home() {
  const [tasks, setTasks] = React.useState<Task[]>([]);

  const getTasks = async () => {
    const response      = await fetch(`${todoApi}/list-tasks/${userId}`);
    const responseData  = await response.json();

    const tasks: Task[] = responseData.tasks;
    setTasks(tasks);
  };

  useEffect(() => {
    getTasks();
  }, []);

  console.log(tasks);

  return (
    <div>
      <Navbar/>
      {
        tasks.map(task => <li> {task.content} </li>)
      }
    </div>
  );
}

export default Home;
