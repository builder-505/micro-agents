# Contributing to Micro-Agents

We love contributions! Our mission is to keep AI agent architectures simple, transparent, and bloat-free.

## Recipe Guidelines
If you want to contribute a new recipe, please adhere to these strict rules:

1. **Under 100 Lines**: Keep core logic concise, readable, and self-contained.
2. **Zero Heavy Frameworks**: No LangChain, AutoGen, or CrewAI. Pure Python standard library or standard API endpoints.
3. **Runnable Out of the Box**: Every recipe must include an offline/mock demonstration so anyone can run it immediately without API keys.
4. **Clean Comments**: Explain the *why* and the architectural pattern, not just the syntax.

## Ideas for Future Recipes
- Human-in-the-loop confirmation gates
- Routing agents with semantic embeddings
- Tree-of-Thought search agent
- Self-evaluating judge agent
- TypeScript / Go / Rust equivalents

## Submission Process
1. Fork the repository
2. Create your feature branch (`git checkout -b recipe/my-new-agent`)
3. Add your recipe in `recipes/`
4. Update the table in `README.md`
5. Open a Pull Request!
