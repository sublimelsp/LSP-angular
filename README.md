# LSP-angular

This is a helper package that automatically installs and updates the [Angular Language Server](https://github.com/angular/vscode-ng-language-service) for you.



## Installation

* Install [LSP](https://packagecontrol.io/packages/LSP), [Ngx HTML](https://packagecontrol.io/packages/Ngx%20HTML) and `LSP-angular` from Package Control.
* Restart Sublime.


## Configuration

Open configuration file using command palette with `Preferences: LSP-angular Settings` command or opening it from the Sublime menu (`Preferences > Package Settings > LSP > Servers > LSP-angular`).


## Different Angular Version

For people who need an older version of the angular server,
this is how to point to a local @angular/language-server.

Override the start command in a ST project file, to point to a local @angular/language-server

```json
{
  "folders": [
    {
      "path": "."
    }
  ],
  "settings": {
    "LSP": {
      "LSP-angular": {
        "command": [
          "${node_bin}",
          "${folder}/node_modules/@angular/language-server/index.js", // maybe adjust the path based on your project
          "--ngProbeLocations", "${folder}/node_modules",  // maybe adjust the path based on your project
          "--tsProbeLocations", "${folder}/node_modules",  // maybe adjust the path based on your project
          "--stdio"
        ]
      },
    }
  }
}
```

An example can be found at https://github.com/sublimelsp/LSP-angular/pull/97#issuecomment-1571887048
