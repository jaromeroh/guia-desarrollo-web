async (page) => {
  const rootUrl = "http://localhost:4000/";
  const consoleErrors = [];
  const pageErrors = [];

  page.on("console", (message) => {
    if (message.type() === "error") {
      consoleErrors.push({ url: page.url(), text: message.text() });
    }
  });
  page.on("pageerror", (error) => {
    pageErrors.push({ url: page.url(), text: error.message });
  });

  await page.goto(rootUrl, { waitUntil: "domcontentloaded" });
  const contentUrls = await page.evaluate(() => {
    const linkedPages = [...document.querySelectorAll(".book-summary a[href]")]
      .map((link) => new URL(link.getAttribute("href"), location.href).href)
      .filter((url) =>
        /\/(?:chapters\/\d{2}-[^/]+|appendices\/[a-e]-[^/]+)\.html$/.test(url)
      );
    return [location.href, ...linkedPages]
      .filter((url, index, all) => all.indexOf(url) === index)
      .sort();
  });

  const modes = [
    { name: "desktop", width: 1280, height: 900 },
    { name: "mobile", width: 390, height: 844 },
  ];
  const reports = [];

  for (const mode of modes) {
    await page.setViewportSize({ width: mode.width, height: mode.height });

    for (const url of contentUrls) {
      await page.goto(url, { waitUntil: "domcontentloaded" });
      if (mode.name === "mobile") {
        await page.evaluate(() => {
          document.querySelector(".book")?.classList.remove("with-summary");
        });
      }

      await page.waitForFunction(
        () => [...document.querySelectorAll(".markdown-section img")].every((image) => image.complete),
        { timeout: 10000 }
      );

      const report = await page.evaluate((modeName) => {
        const section = document.querySelector(".markdown-section");
        const sectionRect = section?.getBoundingClientRect();
        const images = [...document.querySelectorAll(".markdown-section img")];
        const issues = [];

        for (const [index, image] of images.entries()) {
          const rect = image.getBoundingClientRect();
          const picture = image.closest("picture");
          const mobileSource = picture?.querySelector('source[media*="max-width"]')?.srcset || "";
          const currentSrc = image.currentSrc || image.src;
          const label = `${index + 1}: ${currentSrc.split("/").pop()}`;

          if (!image.complete || image.naturalWidth === 0 || image.naturalHeight === 0) {
            issues.push(`${label} no cargó`);
          }
          if (!image.getAttribute("alt")?.trim()) {
            issues.push(`${label} no tiene texto alternativo`);
          }
          if (
            sectionRect &&
            (rect.left < sectionRect.left - 1 || rect.right > sectionRect.right + 1)
          ) {
            issues.push(`${label} desborda horizontalmente el contenido`);
          }
          if (mobileSource) {
            const usesMobile = /-mobile\.svg(?:$|\?)/.test(currentSrc);
            if (modeName === "mobile" && !usesMobile) {
              issues.push(`${label} no activó la variante móvil`);
            }
            if (modeName === "desktop" && usesMobile) {
              issues.push(`${label} activó la variante móvil en escritorio`);
            }
          }
        }

        return {
          title: document.title,
          url: location.href,
          imageCount: images.length,
          issues,
        };
      }, mode.name);

      reports.push({ mode: mode.name, ...report });
    }
  }

  return {
    contentPageCount: contentUrls.length,
    pageLoads: reports.length,
    imageLoads: reports.reduce((total, report) => total + report.imageCount, 0),
    reportsWithIssues: reports.filter((report) => report.issues.length),
    consoleErrors,
    pageErrors,
  };
}
