with import <nixpkgs> {};

let
  myPython = python3.withPackages(p: [ p.flask p.flask_mail p.flask_sqlalchemy p.gunicorn p.qrcode p.requests ] ++ [ p.black p.isort ]);
in
  stdenv.mkDerivation {
    name = "ctjb-dev";
    buildInputs = [ myPython sqlite ];
  }
