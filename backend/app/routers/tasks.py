from typing import Dict
from app.models.tasks import Task
from app.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from db.supabase import create_supabase_client

router = APIRouter(tags=["Task"])

# Initialize supabase client
supabase = create_supabase_client()


# Retrieve all user tasks
@router.get("/tasks")
def get_tasks(token: str = Depends(get_current_user)):
    try:
        # Retrieve user tasks from tasks table
        tasks = (
            supabase.from_("tasks").select("*").eq("user_id", token["sub"]).execute()
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    return tasks


# Create task
@router.post("/create_task")
def create_task(token: str = Depends(get_current_user), task_details: Task = None):
    if not task_details:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Task details are required"
        )
    try:
        task_created = (
            supabase.from_("tasks")
            .insert(
                {
                    "user_id": token["sub"],
                    "text": task_details.text,
                    "completed": task_details.completed,
                }
            )
            .execute()
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    return {
        "message": "Task created successfully",
        "task_id": task_created.data[0]["id"],
    }


# Delete task
@router.delete("/delete_task/{task_id}")
def delete_task(task_id: int, token: str = Depends(get_current_user)):
    try:
        # Delete the task with the given task_id
        deleted_task = (
            supabase.from_("tasks")
            .delete()
            .eq("id", task_id)
            .eq("user_id", token["sub"])
            .execute()
        )

        if len(deleted_task.data) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )
        return {"message": "Task deleted successfully"}

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
