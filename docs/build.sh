mkdir compare
mkdir correspondence
mkdir daybook
mkdir writings


rm -fr compare/*
rm -fr correspondence/*
rm -fr daybook/*
rm -fr writings/*

cd compare-dev
npm run build
cp -R dist/* ../compare/

cd ..

cd correspondence-dev
npm run build
cp -R dist/* ../correspondence/

cd ..

cd daybook-dev
npm run build
cp -R dist/* ../daybook/

cd ..

cd writings-dev
npm run build
cp -R dist/* ../writings/
