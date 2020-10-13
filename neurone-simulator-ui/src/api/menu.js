const Menu = [
  { header: "Menu" },
  /*
  {
    title: "Home",
    group: "apps",
    icon: "mdi-view-dashboard",
    name: "home",
  },
  */
  {
    title: "Start simulation",
    group: "apps",
    icon: "mdi-play-circle",
    name: "simulate"
  },
  {
    title: "Results history",
    group: "apps",
    icon: "mdi-database",
    name: "results-history"
  },
  {
    title: "Results heatmap",
    group: "apps",
    icon: "mdi-fire",
    name: "results-heatmap"
  }
];

// reorder menu
Menu.forEach(item => {
  if (item.items) {
    item.items.sort((x, y) => {
      let textA = x.title.toUpperCase();
      let textB = y.title.toUpperCase();
      return textA < textB ? -1 : textA > textB ? 1 : 0;
    });
  }
});

export default Menu;
