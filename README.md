# Asyncinator

When you want everything to be async, but it's not, you use the asyncinator.

This small service helps make things async. Pass a method, url, some headers and a request body, it'll perform the request and call a callback with the response.

    curl -X POST https://asyncinator.cfapps.io/     \
         -d method=get                              \
         -d url=http://www.google.com/              \
         -d headers=[]                              \
         -d body=null                               \
         -d callback=https://whatever.io/itsdone

The services takes the following arguments:

| Key      | Required? | What's it for?                                                                                     |
|----------|-----------|----------------------------------------------------------------------------------------------------|
| method   | Yes       | The HTTP method to use. Allowed methods are: `GET` `POST` `PUT` `PATCH`                            |
| url      | Yes       | The URL to call                                                                                    |  
| callback | Yes       | The URL to post the response to                                                                    |  
| headers  | No        | A dictionary (in JSON format) of headers to send in the request                                    |  
| body     | No        | A request body                                                                                     |  
| insecure | No        | If set, no certificates will be verified (neither of the server specified in URL nor the callback) |
| salt     | No        | See task_signature docs below.                                                                     |
| context  | No        | Anything at all, really. Asyncinator will send it back to you with the callback                    |

When given a valid request, it will respond with "201 Accepted" and a task ID in the body.

## The callback

Once the request has been performed, asyncinator will POST to the callback URL. The body will be a JSON object with the following keys:

| Key            | Description                                                                               |
|----------------|-------------------------------------------------------------------------------------------|
| task           | The same task ID that was given in response to the original request.                      |
| status         | The HTTP status from the server (e.g. "200 Ok")                                           |
| headers        | A dictionary with the headers of the response from the server                             |
| body           | The response body                                                                         | 
| task_signature | (Only if salt was given original request) See below                           |
| context        | (Only if given in the original request) Exactly what you provided in the original request |

### task_signature
If you pass `salt` in your request, the callback will include a task_signature consisting of sha512(task ID + salt). Only you and asyncinator should be able to know these, so this helps you validate that it's not a fake callback.

Have fun!

