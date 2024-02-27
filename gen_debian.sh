VERSION="0.0.2"
ARCH="all"
DEB_FILE="meshnet_${VERSION}_${ARCH}"
DEB_BUILD_DIR="deb_build/${DEB_FILE}"

echo "Making the deb_build dir"
mkdir -p ${DEB_BUILD_DIR}/opt/
cp -r meshnet/ ${DEB_BUILD_DIR}/opt/

mkdir -p ${DEB_BUILD_DIR}/etc/meshnet/
mkdir -p ${DEB_BUILD_DIR}/opt/meshnet/installation_files
mkdir -p ${DEB_BUILD_DIR}/opt/meshnet/artifacts
mkdir -p ${DEB_BUILD_DIR}/etc/systemd/system/

echo "moving meshnet to deb_build"
cp meshnet/configs/default_configs.toml ${DEB_BUILD_DIR}/etc/meshnet/config.toml
cp meshnet.service ${DEB_BUILD_DIR}/etc/systemd/system/
cp -r packages ${DEB_BUILD_DIR}/opt/meshnet/installation_files
cp honeycomb.png ${DEB_BUILD_DIR}/opt/meshnet/artifacts
cp MeshNet.desktop ${DEB_BUILD_DIR}/opt/meshnet/installation_files
cp uninstall.sh ${DEB_BUILD_DIR}/opt/meshnet/


echo "Copying DEBIAN to deb_build"
cp -r DEBIAN ${DEB_BUILD_DIR}
chmod 555 ${DEB_BUILD_DIR}/DEBIAN/postinst
chmod 555 ${DEB_BUILD_DIR}/DEBIAN/postrm

echo "Running dpkg-deb"
dpkg-deb --build ${DEB_BUILD_DIR}

echo "Cleaning up"

echo "Building .zip package"
rm -r ${DEB_BUILD_DIR}/*
cp install.sh ${DEB_BUILD_DIR}
chmod a+x ${DEB_BUILD_DIR}/install.sh
cp README.md ${DEB_BUILD_DIR}
cp uninstall.sh ${DEB_BUILD_DIR}
chmod a+x ${DEB_BUILD_DIR}/uninstall.sh
cp ${DEB_BUILD_DIR}.deb ${DEB_BUILD_DIR}
cd deb_build
zip -r ${DEB_FILE}.zip ${DEB_FILE}
cd ..
mv ${DEB_BUILD_DIR}.deb ./builds
mv deb_build/${DEB_FILE}.zip ./builds

rm -r deb_build/