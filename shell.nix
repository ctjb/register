with import <nixpkgs> {};

let
  myPython = python3.withPackages(p: [ p.flask p.flask_mail p.flask_sqlalchemy p.gunicorn p.qrcode ]);
in
  stdenv.mkDerivation {
    name = "ctjb-dev";
    buildInputs = [ myPython ];
  }
