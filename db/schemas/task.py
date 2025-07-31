def task_schema(task_data):
    if not task_data:
        return None
    else:
        return {
            "id": str(task_data["_id"]),
            "user_id": task_data["user_id"],
            "name": task_data["name"],
            "date_to_complete": task_data["date_to_complete"],
            "check": task_data["check"]
        }

def task_schema_list(task_list):
    return [task_schema(task) for task in task_list]
