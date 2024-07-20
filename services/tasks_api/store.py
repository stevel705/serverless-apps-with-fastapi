import datetime
from uuid import UUID
import boto3
from boto3.dynamodb.conditions import Key
from models import Task, TaskStatus


class TaskStore:

    def __init__(self, table_name: str):
        self.table_name = table_name

    def add(self, task: Task):
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(self.table_name)
        table.put_item(
            Item={
                "PK": f"#{task.owner}",
                "SK": f"#{task.id}",
                "GS1PK": f"#{task.owner}#{task.status.value}",
                "GS1SK": f"#{datetime.datetime.now(datetime.UTC).isoformat()}",
                "id": str(task.id),
                "title": task.title,
                "status": task.status.value,
                "owner": task.owner,
            }
        )

    def get_by_id(self, task_id: UUID, owner: str) -> Task:
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(self.table_name)
        response = table.get_item(
            Key={
                "PK": f"#{owner}",
                "SK": f"#{task_id}",
            }
        )

        item = response.get("Item")
        if item is None:
            return None

        return Task(
            id=UUID(item["id"]),
            title=item["title"],
            status=TaskStatus(item["status"]),
            owner=item["owner"],
        )

    def list_open(self, owner: str):
        return self._list_by_status(owner, TaskStatus.OPEN)

    def list_closed(self, owner: str):
        return self._list_by_status(owner, TaskStatus.CLOSED)

    def _list_by_status(self, owner: str, status: TaskStatus):
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(self.table_name)
        last_key = None
        query_kwargs = {
            "IndexName": "GS1",
            "KeyConditionExpression": Key("GS1PK").eq(f"#{owner}#{status.value}"),
        }
        tasks = []
        while True:
            if last_key is not None:
                query_kwargs["ExclusiveStartKey"] = last_key
            response = table.query(**query_kwargs)
            tasks.extend(
                [
                    Task(
                        id=UUID(record["id"]),
                        title=record["title"],
                        owner=record["owner"],
                        status=TaskStatus[record["status"]],
                    )
                    for record in response["Items"]
                ]
            )
            last_key = response.get("LastEvaluatedKey")
            if last_key is None:
                break
        return tasks
