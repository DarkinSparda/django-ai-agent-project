from asgiref.sync import async_to_sync
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool, ToolException
from django.db.models import Q
from documents.models import Document

from mypermit import permit_client as permit
@tool
def list_documents(limit: int,config:RunnableConfig):
    """
    Get Documents of the current user (most recent 5)
    """
    if limit > 25:
        limit = 25 # Maximum
    metadata = config.get('configurable') or config.get('metadata')
    user_id = metadata.get('user_id')

    has_perms = async_to_sync(permit.check)(f"{user_id}", "read", "document")
    if not has_perms:
        raise ToolException("You dont have permissions to list docs")

    qs = Document.objects.filter(owner_id=user_id, active=True).order_by("-created_at")[:limit]
    response_data = []
    '''
    {
        "id": 3,
        "title": Harry Poter,
    },
    {
        "id": 6,
        "title": The Unknown,
    }, etc...
    '''
    
    print("Performed List Documents")
    for x in qs:
        response_data.append(
            {
                "id": x.id,
                "title": x.title,
            }
        )

    return response_data

@tool
def get_document(doc_id:int, config:RunnableConfig):
    """
    Get details of a document for current user
    """

    metadata = config.get('configurable') or config.get('metadata')
    user_id = metadata.get('user_id')
    if user_id is None:
        raise ToolException('invalid request for user')
    
    has_perms = async_to_sync(permit.check)(f"{user_id}", "read", "document")
    if not has_perms:
        raise ToolException("You dont have permissions to read docs")

    print("Config: ", config)
    try:
        doc = Document.objects.get(owner=user_id, id=doc_id, active=True)
    except Document.DoesNotExist:
        raise ToolException("Document was not found")
    except:
        raise ToolException("Invalid request in requesting document through id")
    response_data = {
                    "id": doc.id,
                    "title": doc.title,
                    "content": doc.content,
                    }
    print("Performed get Document")
    return response_data


@tool
def create_document(title:str, content: str, config:RunnableConfig):
    """
    Create new document with args:
    title: max 120 chars
    content: long text
    """

    metadata = config.get('configurable') or config.get('metadata')
    user_id = metadata.get('user_id')
    if user_id is None:
        raise ToolException('invalid request for user')
    
    has_perms = async_to_sync(permit.check)(f"{user_id}", "create", "document")
    if not has_perms:
        raise ToolException("You dont have permissions to CREATE docs")


    print("Config: ", config)
    try:
        doc = Document.objects.create(owner_id=user_id, title=title, content=content, active=True)
    except Exception as e:
        raise ToolException(f"Failed to create document: {str(e)}")
    response_data = {
                "id": doc.id,
                "title": doc.title,
                "content": doc.content,
                "created_at": doc.created_at,
                }
    print("Performed CREATE Document")
    return response_data


@tool
def delete_document(doc_id: int, config:RunnableConfig):
    """
    Create new document with args:
    title: max 120 chars
    content: long text
    """

    metadata = config.get('configurable') or config.get('metadata')
    user_id = metadata.get('user_id')
    if user_id is None:
        raise ToolException('invalid request for user')
    
    has_perms = async_to_sync(permit.check)(f"{user_id}", "delete", "document")
    if not has_perms:
        raise ToolException("You dont have permissions to DELETE docs")

    print("Config: ", config)
    try:
        doc = Document.objects.get(id=doc_id, active=True)
        doc.delete()
    except Exception as e:
        raise ToolException(f"Failed to delete document: {str(e)}")
    response_data = {
                "id": doc.id,
                "title": doc.title,
                "content": doc.content,
                "created_at": doc.created_at,
                }
    print("Performed DELETE Document")
    return response_data

@tool
def query_search_documents(text: str, config:RunnableConfig):
    """
    Create new document with args:
    title: max 120 chars
    content: long text
    """

    metadata = config.get('configurable') or config.get('metadata')
    user_id = metadata.get('user_id')
    if user_id is None:
        raise ToolException('invalid request for user')
    default_lookups = {
        'owner_id': user_id,
        'active': True,
    }
    try:
        doc = Document.objects.filter(**default_lookups).filter(
        Q(title__icontains=text) |
        Q(content__icontains=text)
        ).order_by('-created_at')
        matched_doc = doc[0]
    except Exception as e:
        raise ToolException(f"Failed to get document: {str(e)}")
    
    response_data = {
                "id": matched_doc.id,
                "title": matched_doc.title,
                "content": matched_doc.content,
                "created_at": matched_doc.created_at,
                }
    print("Performed SEARCH Document")
    return response_data

document_tools = [
    delete_document,
    create_document,
    list_documents,
    get_document,
    query_search_documents,
]