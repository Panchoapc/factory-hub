from .views import SalesOrderViewSet, ClientViewSet, ProductViewSet

client_list = ClientViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
client_detail = ClientViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
product_list = ProductViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
product_detail = ProductViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
salesorder_list = SalesOrderViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
salesorder_detail = SalesOrderViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
