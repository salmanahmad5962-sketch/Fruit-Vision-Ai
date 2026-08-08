// ════════════════════════════════════════════════
// FRUIT CURSOR — replaces the mouse pointer with a
// small fruit icon, picking a new random fruit on
// every click.
// ════════════════════════════════════════════════
(function () {
  const FRUIT_CURSORS = [
    "./assets/images/cursors/fruit-apple-cursor.png",
    "./assets/images/cursors/fruit-banana-cursor.png",
    "./assets/images/cursors/fruit-peach-cursor.png",
    "./assets/images/cursors/fruit-grapes-cursor.png",
    "./assets/images/cursors/fruit-watermelon-cursor.png",
  ];

  let lastIndex = -1;

  function pickNewFruit() {
    let index;
    do {
      index = Math.floor(Math.random() * FRUIT_CURSORS.length);
    } while (index === lastIndex && FRUIT_CURSORS.length > 1);
    lastIndex = index;
    return FRUIT_CURSORS[index];
  }

  function applyFruitCursor() {
    const fruit = pickNewFruit();
    // 18 18 centers the cursor hotspot roughly in the middle of the 36x36 icon
    document.documentElement.style.cursor = `url('${fruit}') 18 18, auto`;
    document.body.style.cursor = `url('${fruit}') 18 18, auto`;
  }

  document.addEventListener("DOMContentLoaded", applyFruitCursor);
  document.addEventListener("click", applyFruitCursor);
})();
