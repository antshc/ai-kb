# C# LSP Servers: `csharp-ls` vs `roslyn-language-server` vs `dnx`

## Short Answer

If you are choosing for **Copilot CLI** or modern editor integration:

- **Best for Copilot CLI:** `roslyn-language-server`
- **Best integration with VS Code:** official Microsoft C# extension / C# Dev Kit (which uses Roslyn-based tooling under the hood)
- **What is `dnx`?** Not an LSP server — just a runner for .NET tools

So the practical recommendation is:

```text
Use roslyn-language-server for Copilot CLI.
Use C# Dev Kit in VS Code.
Do not think of dnx as a language server.
```

## What each thing is

### `csharp-ls`

`csharp-ls` is a **community-maintained** C# Language Server Protocol (LSP) server.

It is designed to provide common IDE features such as:

- completion
- diagnostics
- symbol lookup
- navigation
- some refactoring support

It is useful for generic LSP clients and lightweight editor setups.

In simple terms:

```text
csharp-ls = "an alternative C# language server"
```

### `roslyn-language-server`

`roslyn-language-server` is the **Roslyn-based** C# language server aligned with the Microsoft ecosystem.

This is the more “official-direction” option because it is based on the same Roslyn compiler/platform stack used by Microsoft tooling.

In simple terms:

```text
roslyn-language-server = "the Microsoft/Roslyn-style C# language server"
```

It is generally a better fit if you want:

- more correct semantic understanding
- better parity with modern .NET tooling
- better compatibility with the direction of Microsoft editor tooling

### `dnx`

`dnx` is **not** a language server.

It is just a **runner** for .NET tools.

For example:

```bash
dnx roslyn-language-server --stdio
```

This means:

```text
"Run the roslyn-language-server tool through the .NET tool executor"
```

So:

```text
dnx != LSP server
dnx = launcher / execution wrapper
```

## Main difference in practice

The real comparison is:

```text
csharp-ls  vs  roslyn-language-server
```

Not:

```text
csharp-ls  vs  dnx
```

Because `dnx` is just how you may launch `roslyn-language-server`.

## Which is better for Copilot CLI?

## Recommendation: `roslyn-language-server`

If your goal is to use a C# LSP with **Copilot CLI**, then `roslyn-language-server` is the better choice.

### Why

Because Copilot / agent-style tooling benefits from:

- accurate semantic understanding
- better symbol resolution
- stronger project awareness
- behavior closer to official C# tooling

That usually favors Roslyn-based infrastructure.

### Why not default to `csharp-ls`

`csharp-ls` can work, but in practice it is more of a:

- lightweight
- community
- generic-editor

solution.

That makes it fine for some setups, but less ideal if your goal is:

```text
"Make AI coding tools understand my real .NET solution as correctly as possible"
```

## Which integrates better with VS Code?

## Recommendation: official C# extension / C# Dev Kit

For **VS Code**, the best integration is not “manual `csharp-ls` setup”.

The best integration is:

- Microsoft C# extension
- C# Dev Kit

That is the native, supported, best-integrated experience.

### Why

Because VS Code integration is not only about LSP.

It also includes:

- project loading
- debugging
- test discovery
- solution awareness
- Razor / ASP.NET support
- editor-specific behavior
- .NET workspace services

So even if both servers can technically speak LSP, the official VS Code experience is much broader than “just a language server”.

## Recommended setup by use case

### If you use Copilot CLI in terminal / WSL

Use:

```text
roslyn-language-server
```

Why:

- better semantic fit
- closer to official .NET tooling
- better future-proof choice

### If you use VS Code for coding

Use:

```text
C# Dev Kit / official Microsoft C# extension
```

Why:

- best editor integration
- easiest experience
- most complete feature set

### If you want a minimal generic LSP setup

Use:

```text
csharp-ls
```

Why:

- simpler mental model
- editor-agnostic
- okay for lightweight workflows

But it is usually not the strongest option for AI-assisted coding.

## Practical ranking

If your goal is **AI coding + modern .NET projects**:

| Option | Best for | Pros | Cons |
| --- | --- | --- | --- |
| `roslyn-language-server` | Copilot CLI / AI coding / modern .NET | Best semantic quality, Microsoft-aligned | Can be less straightforward to configure manually |
| Official VS Code C# / C# Dev Kit | VS Code development | Best overall experience in VS Code | Editor-specific, not a generic CLI LSP setup |
| `csharp-ls` | Lightweight generic LSP usage | Simple, editor-agnostic | Less aligned with official tooling, may be less reliable for AI tooling |
| `dnx` | Launching tools | Convenient execution | Not an LSP server |

## Best recommendation for you

Since you are using:

- .NET
- WSL
- Copilot CLI
- VS Code

the best split is:

### In Copilot CLI

Use:

```text
roslyn-language-server
```

### In VS Code

Use:

```text
C# Dev Kit / official C# extension
```

### Avoid this mistake

Do **not** think:

```text
"I need to choose between dnx and roslyn-language-server"
```

That is like choosing between:

```text
"the app" vs "the command used to start the app"
```

Correct mental model:

```text
roslyn-language-server = the server
dnx = how you launch it
```

## Final recommendation

If you want one clean answer:

```text
For Copilot CLI -> use roslyn-language-server
For VS Code -> use official C# Dev Kit
Use csharp-ls only if you want a simpler fallback
dnx is only a launcher
```

## One-line summary

```text
csharp-ls = community LSP
roslyn-language-server = better modern/default choice
dnx = just the runner
VS Code = use official Microsoft C# tooling
```
