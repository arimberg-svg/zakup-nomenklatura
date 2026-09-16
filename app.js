(() => {
  const topics = [...document.querySelectorAll("details.topic")];

  function openTopic(id, scroll) {
    const el = document.getElementById(id);
    if (!el) return;
    topics.forEach((t) => {
      t.open = t === el;
    });
    if (scroll) el.scrollIntoView({ behavior: "smooth", block: "start" });
    history.replaceState(null, "", "#" + id);
  }

  document.querySelectorAll("[data-open]").forEach((a) => {
    a.addEventListener("click", (e) => {
      e.preventDefault();
      openTopic(a.getAttribute("data-open"), true);
    });
  });

  topics.forEach((t) => {
    t.addEventListener("toggle", () => {
      if (!t.open) return;
      topics.forEach((o) => {
        if (o !== t) o.open = false;
      });
      history.replaceState(null, "", "#" + t.id);
    });
  });

  const hash = decodeURIComponent(location.hash.replace("#", ""));
  if (hash) openTopic(hash, false);
})();
