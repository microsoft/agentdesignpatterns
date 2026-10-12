let mermaidModule;

document$.subscribe(async () => {
  try {
    mermaidModule ??= import(
      "https://unpkg.com/mermaid@11/dist/mermaid.esm.min.mjs"
    );
    const { default: mermaid } = await mermaidModule;
    mermaid.initialize({ startOnLoad: false });
    await mermaid.run({
      nodes: document.querySelectorAll(".mermaid"),
    });
  } catch (error) {
    console.error("Unable to render Mermaid diagrams.", error);
  }
});
