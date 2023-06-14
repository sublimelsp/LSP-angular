# LSP-angular

This is a helper package that automatically installs and updates the [Angular Language Server](https://github.com/angular/vscode-ng-language-service) for you.



## Installation

* Install [LSP](https://packagecontrol.io/packages/LSP), [Ngx HTML](https://packagecontrol.io/packages/Ngx%20HTML) and `LSP-angular` from Package Control.
* Restart Sublime.


## Configuration

Open configuration file using command palette with `Preferences: LSP-angular Settings` command or opening it from the Sublime menu (`Preferences > Package Settings > LSP > Servers > LSP-angular`).


## Versioning

This language service extension relies on the `@angular/language-server` and `typescript` packages for its backend.
`@angular/language-server` is always bundled with the extension, and is always the latest version at the time of the release.

For people who need an older version of the angular server,
this is how to point to a local `@angular/language-server`.

Override the start command in a ST project file, to point to a local `@angular/language-server`

```javascript
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
          "${folder}/node_modules/@angular/language-server/index.js", // adjust the path based on your project
          "--ngProbeLocations", "${folder}/node_modules",  // adjust the path based on your project
          "--tsProbeLocations", "${folder}/node_modules",  // adjust the path based on your project
          "--stdio"
        ]
      },
    }
  }
}
```
