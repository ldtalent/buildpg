buildpg
=======

compiles a django website into a phonegap app

Up until now it has been impossible to develop once and get both fantastic SEO for your content rich site and a fast HTML5 app that isn't just a webview (note, Apple does not like webviews). 

Introducing buildpg...

`WARNING: THIS PROJECT IS STILL SPECIFIC TO THE LEARNING DOLLARS IMPLEMENTATION. WE WILL BE MAKING IT GENERALIZABLE SHORTLY. IN THE MEANTIME, FEEL FREE TO TWEAK TO SUIT YOUR PROJECT. ALSO WE ARE WORKING ON THE "TEMPORARILY" PART (6.b). We'll tackle the usage question then.`

Prerequisites:

1. You must use Django.

2. You must use Pyjade but recognize that Django and Pyjade template logic and template variables will be omitted from the PhoneGap compilation so you must compensate with Javascript (and api calls). You should structure your Javascript pages as follows:
    
    ```javascript
    function isPhoneGap() {
        return document.URL.indexOf('http://') === -1 && document.URL.indexOf('https://') === -1;
    }

    if (isPhoneGap()) {
        // fill in all template variables
        // handle all template logic
    }

    // rest of js code
    ```

3. You must have jade installed (install nodejs and then npm install jade -g [sudo if necessary])

4. We expect a layout like:

    - YOUR_DJANGO_PROJECT
        - templates
            - template_that_i_want_compiled-1.jade
            - template_that_i_want_compiled-2.jade
            - partials
                - head.jade
                - partial_that_i_want_included_in_templates-1.jade
                - partial_that_i_want_included_in_templates-2.jade
        - static
            - css
            - img
            - js
            - compiled-partials
        - YOUR_APP_1
            - templates
                - template_that_i_want_compiled-3.jade
                - template_that_i_want_compiled-4.jade
                - partials
                    - partial_that_i_want_included_in_templates-5.jade
                    - partial_that_i_want_included_in_templates-6.jade
            - static
                - css
                - img
                - js
                - compiled-partials
        - YOUR_APP_2
            - templates
                - template_that_i_want_compiled-7.jade
                - template_that_i_want_compiled-8.jade
                - partials
                    - partial_that_i_want_included_in_templates-9.jade
                    - partial_that_i_want_included_in_templates-10.jade
            - static
                - css
                - img
                - js
                - compiled-partials

5. All static files and all jade files should have unique base names.

6. A quick under-the-hood:
    
    a. We copy over static files from `YOUR_DJANGO_PROJECT/static` and from the `static` directories of each member of `YOUR_DJANGO_APPS` into `YOUR_PHONEGAP_APP/www/static`.
    
    b. Using the jade compiler (not the pyjade compiler), we compile all the templates that sit directly in `YOUR_DJANGO_PROJECTS/templates` and in the `templates` directories of each member of `YOUR_DJANGO_APPS`. We put these compiled html files in `YOUR_PHONEGAP_APP/www` (be careful to not have any file called `index.jade`) We do temporarily make a copy of your templates in `YOUR_PHONEGAP_APP` in order to remove pyjade template logic.
    
    c. We compile your `head.jade` file into the `index.html` file of the PhoneGap app (this should have all the script includes and the css links).
    
    d. We make static file imports relative (change "/static" to "static") and remove Django template logic for files in `YOUR_PHONEGAP_APP/www/static/js`, `YOUR_PHONEGAP_APP/www/static/css`, and `YOUR_PHONEGAP_APP/static/compiled-partials` directory, as well as for html files in `YOUR_PHONEGAP_APP/www`. (We expect all your javascript static file requests will be of the form `$.get('/static/...', callback)`)
    
    e. We expect the following function to sit in the index.js autocreated by phonegap:

    ```javascript
    function pgget(url, data, success, dataType) { // define a get request that removes the slash from /static gets, http://api.jquery.com/jquery.get/
        if (url.substring(0, 7) == '/static') url = 'file:///android_asset/www/' + url.substring(1);
        $.get(url, data, success, dataType);
    }
    ```

7. We recommend using jQuery Mobile.

8. As you develop, test each feature you add both on web and on mobile at the same time.
