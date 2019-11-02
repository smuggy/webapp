#!/usr/bin/env sh
set -x
set -e

function set_version() {
    os=`uname`
    version_string=`grep app_version app.ini`
    version=${version_string#app_version: }
    if [ "$os" == "Darwin" ] ; then
        sed -i "" -e s/^app_version.\*/app_version=\"${version}\"/ app/webapp.py
        sed -i "" -e s/^version.\*/version:\ \"${version}\"/ chart/simpleweb/Chart.yaml
    else
        sed -i -e s/^app_version.\*/app_version=\"${version}\"/ app/webapp.py
        sed -i -e s/^version.\*/version:\ \"${version}\"/ chart/simpleweb/Chart.yaml
    fi

    image_tag_string=`grep image_tag app.ini`
    image_tag=${image_tag_string#image_tag: }
    if  [ "$os" == "Darwin" ] ; then
        sed -i "" -e s/^\ \ tag:.\*/\ \ tag:\ ${image_tag}/ chart/simpleweb/values.yaml
    else
        sed -i -e s/^\ \ tag:.\*/\ \ tag:\ ${image_tag}/ chart/simpleweb/values.yaml
    fi
}
function build_package() {
    pip3 freeze > requirements.txt
    python3 setup.py bdist_wheel
}
function build_image() {
    docker build --build-arg appversion=${version} -t simpleweb .
    docker tag simpleweb mmckernan/simpleweb:${image_tag}
    docker push mmckernan/simpleweb:${image_tag}
}
function build_chart() {
    helm package chart/simpleweb/    
}

set_version
build_package
build_image
build_chart
