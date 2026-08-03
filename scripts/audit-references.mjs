import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";

const root = process.cwd();
const contentDirectories = [
  ["chapters", path.join(root, "chapters")],
  ["appendices", path.join(root, "appendices")],
];
const outputArgument = process.argv.find((argument) =>
  argument.startsWith("--output="),
);
const dateArgument = process.argv.find((argument) =>
  argument.startsWith("--date="),
);
const outputPath = path.resolve(
  root,
  outputArgument?.slice("--output=".length) ??
    "docs/AUDITORIA-REFERENCIAS.md",
);
const verificationDate = dateArgument?.slice("--date=".length) ??
  new Date().toISOString().slice(0, 10);

// Algunas fuentes públicas bloquean clientes automatizados. Solo se incluyen
// aquí después de comprobar manualmente que el recurso existe y es público.
const manuallyVerifiedUrls = new Set([
  "https://openai.com/index/harness-engineering/",
]);

const standardHosts = new Set([
  "cheatsheetseries.owasp.org",
  "csrc.nist.gov",
  "cwe.mitre.org",
  "datatracker.ietf.org",
  "dom.spec.whatwg.org",
  "ecma-international.org",
  "fetch.spec.whatwg.org",
  "graphql.org",
  "html.spec.whatwg.org",
  "json-schema.org",
  "modelcontextprotocol.io",
  "openid.net",
  "opencontainers.org",
  "owasp.org",
  "spec.whatwg.org",
  "spec.openapis.org",
  "tc39.es",
  "url.spec.whatwg.org",
  "wasi.dev",
  "www.rfc-editor.org",
  "www.w3.org",
]);

const originalSourceHosts = new Set([
  "8thlight.com",
  "adr.github.io",
  "alistair.cockburn.us",
  "c4model.com",
  "kentcdodds.com",
  "martinfowler.com",
  "trunkbaseddevelopment.com",
]);

const primaryDocumentationHosts = new Set([
  "about.gitlab.com",
  "alembic.sqlalchemy.org",
  "anthropic.com",
  "component-model.bytecodealliance.org",
  "cloud.google.com",
  "code.claude.com",
  "curl.se",
  "developer.hashicorp.com",
  "developer.mozilla.org",
  "docs.astral.sh",
  "docs.pydantic.dev",
  "docs.pytest.org",
  "docs.python.org",
  "docs.sigstore.dev",
  "docs.sqlalchemy.org",
  "developers.cloudflare.com",
  "docs.aws.amazon.com",
  "docs.bullmq.io",
  "docs.docker.com",
  "docs.gitlab.com",
  "docs.github.com",
  "docs.nestjs.com",
  "docs.railway.app",
  "docs.railway.com",
  "expressjs.com",
  "fastapi.tiangolo.com",
  "fidoalliance.org",
  "fly.io",
  "firefox-source-docs.mozilla.org",
  "git-scm.com",
  "getpino.io",
  "github.com",
  "go.dev",
  "grafana.com",
  "kubernetes.io",
  "www.linuxfoundation.org",
  "learn.microsoft.com",
  "nextjs.org",
  "nodejs.org",
  "openai.com",
  "opentelemetry.io",
  "playwright.dev",
  "pkg.go.dev",
  "pnpm.io",
  "podman.io",
  "prometheus.io",
  "react.dev",
  "render.com",
  "redis.io",
  "securityscorecards.dev",
  "slsa.dev",
  "socket.io",
  "svelte.dev",
  "tailwindcss.com",
  "tanstack.com",
  "testing-library.com",
  "trivy.dev",
  "trpc.io",
  "vercel.com",
  "vitest.dev",
  "v0.dev",
  "web.dev",
  "webkit.org",
  "www.anthropic.com",
  "www.apollographql.com",
  "www.postgresql.org",
  "www.prisma.io",
  "www.pulumi.com",
  "www.rabbitmq.com",
  "www.who.int",
  "www.zaproxy.org",
  "launchdarkly.com",
  "nodeshift.dev",
  "oauth.net",
  "opentofu.org",
  "packaging.python.org",
]);

function formatDate(date) {
  return new Intl.DateTimeFormat("es-ES", {
    day: "numeric",
    month: "long",
    timeZone: "UTC",
    year: "numeric",
  }).format(new Date(`${date}T12:00:00Z`));
}

function escapeTableCell(value) {
  return value.replaceAll("|", "\\|").replaceAll("\n", " ").trim();
}

function sourceLabel(entry, url) {
  const withoutMarkdownLink = entry.replace(
    /\[([^\]]+)\]\(https?:\/\/[^)]+\)/g,
    "$1",
  );
  const withoutBareUrl = url
    ? withoutMarkdownLink.replace(url, "")
    : withoutMarkdownLink;

  return withoutBareUrl
    .replace(/^\s*-\s*/, "")
    .replace(/\s+[—-]\s*$/, "")
    .trim();
}

function classify(url) {
  if (!url) {
    return "Referencia bibliográfica";
  }

  const host = new URL(url).hostname;

  if (standardHosts.has(host)) {
    return "Estándar u organismo";
  }
  if (primaryDocumentationHosts.has(host)) {
    return "Documentación primaria";
  }
  if (originalSourceHosts.has(host)) {
    return "Fuente original del concepto";
  }
  return "Perspectiva o fuente secundaria";
}

async function collectReferences() {
  const references = [];

  for (const [group, directory] of contentDirectories) {
    const files = (await fs.readdir(directory))
      .filter((file) => file.endsWith(".md"))
      .sort();

    for (const file of files) {
      const auditAllExternalLinks = group === "appendices";
      const contents = await fs.readFile(
        path.join(directory, file),
        "utf8",
      );
      const lines = contents.split("\n");
      let insideReferences = false;

      for (let index = 0; index < lines.length; index += 1) {
        const line = lines[index];

        if (/^## .*Referencias/i.test(line)) {
          insideReferences = true;
          continue;
        }
        if (
          insideReferences &&
          (/^## /.test(line) || /^---$/.test(line))
        ) {
          insideReferences = false;
        }

        const urlMatch = line.match(/https?:\/\/[^\s)>\]]+/);
        if (
          !/^\s*-\s+/.test(line) ||
          (!insideReferences && !(auditAllExternalLinks && urlMatch))
        ) {
          continue;
        }

        const url = urlMatch?.[0].replace(/[.,;:]+$/, "") ?? null;

        references.push({
          chapter: `${group}/${file}`,
          entry: line,
          line: index + 1,
          type: classify(url),
          url,
        });
      }
    }
  }

  return references;
}

async function fetchStatus(url, attempt = 1) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 12_000);

  try {
    const response = await fetch(url, {
      headers: {
        accept: "text/html,application/xhtml+xml,application/pdf,*/*",
        "user-agent": "Mozilla/5.0 editorial-reference-audit/1.0",
      },
      redirect: "follow",
      signal: controller.signal,
    });
    await response.body?.cancel();

    if (response.status >= 500 && attempt < 2) {
      return fetchStatus(url, attempt + 1);
    }

    return {
      finalUrl: response.url,
      status: response.status,
    };
  } catch (error) {
    if (attempt < 2) {
      return fetchStatus(url, attempt + 1);
    }
    return {
      error: error instanceof Error ? error.name : "Error",
      finalUrl: url,
      status: null,
    };
  } finally {
    clearTimeout(timeout);
  }
}

async function verifyUrls(references) {
  const uniqueUrls = [...new Set(
    references.flatMap((reference) =>
      reference.url ? [reference.url] : []
    ),
  )];
  const results = new Map();
  let cursor = 0;

  async function worker() {
    while (cursor < uniqueUrls.length) {
      const url = uniqueUrls[cursor];
      cursor += 1;
      results.set(url, await fetchStatus(url));
    }
  }

  await Promise.all(Array.from({ length: 10 }, () => worker()));
  return results;
}

function renderReport(references, results) {
  const checkedDate = formatDate(verificationDate);
  const webReferences = references.filter((reference) => reference.url);
  const failures = webReferences.filter((reference) => {
    if (manuallyVerifiedUrls.has(reference.url)) {
      return false;
    }
    const status = results.get(reference.url);
    return !status?.status || status.status >= 400;
  });
  const chapters = new Map();
  for (const reference of references) {
    const chapterReferences = chapters.get(reference.chapter) ?? [];
    chapterReferences.push(reference);
    chapters.set(reference.chapter, chapterReferences);
  }
  const lines = [
    "# Auditoría de referencias",
    "",
    `> Corte editorial: ${checkedDate}.`,
    "",
    `Se revisaron **${references.length} referencias** en ${
      chapters.size
    } archivos de contenido: **${webReferences.length} enlaces** y **${
      references.length - webReferences.length
    } referencias bibliográficas sin URL**.`,
    "",
    "La comprobación de un enlace confirma accesibilidad y destino, no la",
    "corrección de todas las afirmaciones que lo citan. Las fuentes volátiles",
    "deben volver a verificarse en la siguiente edición.",
    "",
    "## Criterios",
    "",
    "- **Estándar u organismo:** especificación o publicación de una entidad normativa.",
    "- **Documentación primaria:** documentación mantenida por el proyecto o proveedor.",
    "- **Fuente original del concepto:** publicación del autor o sitio que introdujo la idea.",
    "- **Perspectiva o fuente secundaria:** artículo interpretativo; no debe sostener por sí solo una afirmación normativa.",
    "- **Referencia bibliográfica:** libro u obra sin URL comprobable desde esta auditoría.",
    "",
  ];

  for (const [chapter, chapterReferences] of chapters) {
    lines.push(`## ${chapter.replace(/\.md$/, "")}`, "");
    lines.push("| # | Fuente | Tipo | Resultado |");
    lines.push("|---:|---|---|---|");

    chapterReferences.forEach((reference, index) => {
      const label = escapeTableCell(
        sourceLabel(reference.entry, reference.url),
      );
      let result = "Referencia bibliográfica; comprobar edición";
      let displayedSource = label;

      if (reference.url) {
        const status = results.get(reference.url);
        displayedSource = `[${label}](${reference.url})`;

        if (manuallyVerifiedUrls.has(reference.url)) {
          result = `Disponible; verificación manual tras bloqueo HTTP ${
            status?.status ?? "del cliente automático"
          }; ${checkedDate}`;
        } else if (status?.status && status.status < 400) {
          const redirected = status.finalUrl !== reference.url
            ? "; redirección válida"
            : "";
          result = `Disponible (HTTP ${status.status}${redirected}); ${checkedDate}`;
        } else {
          result = `Revisar (${
            status?.status ? `HTTP ${status.status}` : status?.error ?? "error"
          }); ${checkedDate}`;
        }
      }

      lines.push(
        `| ${index + 1} | ${displayedSource} | ${reference.type} | ${result} |`,
      );
    });

    lines.push("");
  }

  lines.push("## Resultado", "");
  if (failures.length === 0) {
    lines.push(
      `Los ${webReferences.length} enlaces bibliográficos respondieron sin errores HTTP.`,
    );
  } else {
    lines.push(
      `Quedaron ${failures.length} enlaces por revisar antes de publicar.`,
    );
  }
  lines.push("");

  return {
    failures,
    markdown: `${lines.join("\n")}\n`,
    webReferenceCount: webReferences.length,
  };
}

const references = await collectReferences();
const results = await verifyUrls(references);
const report = renderReport(references, results);

await fs.mkdir(path.dirname(outputPath), { recursive: true });
await fs.writeFile(outputPath, report.markdown, "utf8");

console.log(
  `Referencias: ${references.length}; enlaces: ${report.webReferenceCount}; ` +
    `fallos: ${report.failures.length}`,
);
console.log(`Informe: ${path.relative(root, outputPath)}`);

process.exitCode = report.failures.length === 0 ? 0 : 1;
