"""Methods implementing UPnP requests."""
from async_upnp_client import UpnpFactory
from async_upnp_client.aiohttp import UpnpEventHandler
from async_upnp_client.aiohttp import AiohttpRequester

from .constants import (
    BROWSE_CHILDREN,
    CONTENT_DIRECTORY
)

async def browse(location, object_id=0, browse_flag=BROWSE_CHILDREN, filter='*', starting_index=0, requested_count=0, sort_criteria=''):
    requester = AiohttpRequester()
    factory = UpnpFactory(requester)
    device = await factory.async_create_device(location)
    service = device.service(CONTENT_DIRECTORY)
    action = service.action('Browse')
    response = await action.async_call(ObjectID=object_id, BrowseFlag=browse_flag, Filter=filter, StartingIndex=starting_index, RequestedCount=requested_count, SortCriteria=sort_criteria)
    return response['Result']
