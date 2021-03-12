# nginx-stream-controller

As someone who primiarly does most of their work in C++, C, and Python, web languages are not my best thing. This was my first attempt using Flask
to create a web application, so I apologize for its inefficiencies. 

This was written to solve a problem with my Church's live stream workflow. We use OBS to send our stream to a Raspberry Pi 4 running an Nginx server
using the RTMP plugin. This plugin forwards all streams in the `nginx.conf` file. Rather than manually SSHing into the Raspberry Pi, editing the file, and then restarting
the Nginx service - I made this web app to facilitate all this for me.

## Pre-requisites
`pip3 install -r requirements.txt`

This installs the latest version of Flask and crossplane, which are
the only two requirements for this application to work.

## How It Works
Simply name your application. This is what dictates what URL you would enter locally to retrieve the stream.

Example:
If your application name is `live`, then the URL to view the stream on your local network would be `rtmp://{ip-address-of-nginx-server}/live/{stream-key-from-obs}`

You can also change the listening port, and chunk size. This normally remains with the default value of 1935 and 4000, respectively.

You can also toggle the streams on an off using the toggle switch.

Finally, all streaming destinations get added in the `Pushed Streams` section. Any stream added here is where the server will forward your stream.

## Finalizing
Once you have everything configured the way you like, hit the `update` button. This writes the new configuration file.
Hit `Restart` to restart the Nginx service.

## Customizing
You can change the page logo by replacing the `logo.png` file in the static directory.
All other modifications can be made in the `index.html` template and the corresponding stylesheet.
