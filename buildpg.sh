# this script is to be run from ld (the root of the root repo)
apps=(ldapp basicEnglish)

echo 'mimic the server side static'
echo ----------
cp -r ldapp/static/ ldmobile/www/static
for i in ${apps[@]} 
do
    app=$i
    echo $app
    echo -----
    for dir in `ls -d ldapp/$app/static/*/`; do
        echo 'SRC DIR'
        echo $dir
        base_dir=`basename $dir`
        echo 'DST DIR'
        echo ldmobile/www/static/$base_dir/
        cp -r $dir* ldmobile/www/static/$base_dir/
        echo --
    done
    echo -----
done

echo "compile the server side templates to html (we don't compile partials since they are already included)"
echo ----------
cp -r ldapp/templates/ ldmobile/templates
for i in ${apps[@]} 
do
    app=$i
    echo $app
    echo -----
    for template in `ls ldapp/$app/templates/$app/*.jade`; do
        echo 'TEMPLATE'
        echo $template
        echo 'DST DIR: ldmobile/templates/'
        cp $template ldmobile/templates/
        echo --
    done
    echo -----
done

for i in ${apps[@]} 
do
    app=$i
    echo $app
    echo -----
    for template in `ls ldapp/$app/templates/$app/partials/*.jade`; do
        echo 'PARTIAL'
        echo $template
        echo 'DST DIR: ldmobile/templates/partials/'
        cp $template ldmobile/templates/partials/
        echo --
    done
    echo -----
done

for tmpl in `ls ldmobile/templates/*.jade`; do
    echo $tmpl
    echo -----
    python scripts-for-local-use/buildpg/fix_includes.py $tmpl
    rm $tmpl
    mv $tmpl.new $tmpl
    echo -----
done

for tmpl in `ls ldmobile/templates/partials/*.jade`; do
    echo $tmpl
    echo -----
    python scripts-for-local-use/buildpg/fix_includes.py $tmpl true
    rm $tmpl
    mv $tmpl.new $tmpl
    echo -----
done

echo 'compiling jade to html'
echo ----------
for tmpl in `ls ldmobile/templates/*.jade`; do
    echo $tmpl
    tmpl_base=`basename $tmpl`
    if [ $tmpl_base != "index.jade" ]; then
        #echo 'NOT index.jade'
        jade $tmpl -P -o ldmobile/www
    fi
done

echo 'creating head.html for use in creating phonegap index.html'
jade ldmobile/templates/partials/head.jade -P -o ldmobile/www
echo ----------

echo 'removing django templating from html'
python scripts-for-local-use/buildpg/clean_html.py
echo ----------

echo 'deleting head.html after used'
rm ldmobile/www/head.html
echo ----------
