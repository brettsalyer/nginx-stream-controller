function removeStream(item) {
    console.log("Removing " + item.value);
    itemToBeRemoved = document.getElementById(item);
    console.log("Item to be removed", itemToBeRemoved);
    itemToBeRemoved.remove();
  }