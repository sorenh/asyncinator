When you want everything to be async, but it's not, you use the asyncinator.

This small service helps make things async. Pass a method, url, some headers and a request body, it'll perform the request and call a callback with the response.

    curl -X POST https://asyncinator.cfapps.io/     \
         -d method=get                              \
         -d url=http://www.google.com/              \
         -d headers=[]                              \
         -d body=null                               \
         -d callback=https://soren-debug.cfapps.io/
