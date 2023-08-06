#############
tw5-server
#############

`tw5-server` is a TiddlySpot like server to save TiddlyWiki file online.


***********
Install
***********


.. code:: bash

    $: pip install tw5-server


**************
Configuration
**************

* `WIKI_ROOT` where to save wiki files
* `AUTH_BASIC_USER_FILE` file contains view_key and write_key


*********
Tutorial
*********


1. Create wiki named demo

   .. code:: bash

      tw5-server ) WIKI_ROOT=/tmp/wiki_root FLASK_APP=tw5_server/app.py flask create-wiki demo
      wiki "demo" is created. Dir is /tmp/wiki_root/demo
      tw5-server ) cd /tmp/wiki_root/demo
      demo ) tree
      .
      └── index.html
      
      0 directories, 1 file
      demo ) git log
      commit ab08b0d2a903754a8b2a63d86f715ba87d9b1bed (HEAD -> master)
      Author: tw5-server <>
      Date:   Mon Feb 1 13:49:52 2021 +0800
      
          automatic create

2. Set basic auth

   .. code:: ini

      [demo]
      view_key=demo_view_key
      write_key=demo_write_key

3. Run server

   .. code:: bash

      tw5-server ) WIKI_ROOT=/tmp/wiki_root AUTH_BASIC_USER_FILE=basic_auth.ini FLASK_APP=tw5_server/app.py flask run
       * Serving Flask app "tw5_server/app.py"
       * Environment: production
         WARNING: This is a development server. Do not use it in a production deployment.
         Use a production WSGI server instead.
       * Debug mode: off
       * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

4. Open browser and visit `http://127.0.0.1:5000/demo`. Enter the view_key as basic auth and you can see the wiki now.
5. Configure `TiddlySpot` Saver. Set server url as `http://127.0.0.1:5000/demo/store` and paste write_key as password. Then press the `Save Changes` button and the wiki will be saved to local server.
