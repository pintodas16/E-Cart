const slides = Array.from(document.querySelectorAll(".slide-img"));
const slider = document.querySelector(".slider-container");
const buttons = document.querySelectorAll(".slide-buttons div");
const dotEl = document.querySelector(".slide-dots");

console.log(slider);
console.log(slides);
console.log(buttons);
console.log(dotEl);

console.log(dotEl);
let timeoutId;
// console.log(slides);

function getNextPrev() {
  const activeSlide = document.querySelector(".slide-img.active");
  //   console.log(activeSlide);
  const activeIndex = slides.indexOf(activeSlide);

  // next
  if (activeIndex === slides.length - 1) {
    // console.log("match");
    next = slides[0];
  } else {
    next = slides[activeIndex + 1];
  }
  //previous
  if (activeIndex === 0) {
    previous = slides[slides.length - 1];
  } else {
    previous = slides[activeIndex - 1];
  }

  return [next, previous];
}

function getPosition() {
  const activeSlide = document.querySelector(".slide-img.active");
  const activeIndex = slides.indexOf(activeSlide);
  const [next, previous] = getNextPrev();

  slides.forEach((slide, index) => {
    if (index === activeIndex) {
      slide.style.transform = "translateX(0)";
    } else if (slide === previous) {
      slide.style.transform = "translateX(-100%)";
    } else if (slide === next) {
      slide.style.transform = "translateX(100%)";
    } else {
      slide.style.transform = "translateX(100%)";
    }

    slide.addEventListener("transitionend", () => {
      slide.classList.remove("s-top");
    });
  });
}

getPosition();

buttons.forEach((button) => {
  button.addEventListener("click", () => {
    if (button.classList.contains("slide-next")) {
      getNextSlide();
    } else if (button.classList.contains("slide-previous")) {
      getPrevSlide();
    }
  });
});

function getNextSlide() {
  clearTimeout(timeoutId);
  const current = document.querySelector(".slide-img.active");
  const [next, prev] = getNextPrev();

  if (current.classList.contains("s-top")) {
    return;
  }

  next.classList.add("s-top");
  current.classList.add("s-top");
  current.classList.remove("active");
  current.style.transform = "translate(-100%)";
  next.style.transform = "translate(0%)";
  next.classList.add("active");

  getPosition();
  getActiveDots();
  autoLoop();

  console.log("get next slide ");
}
function getPrevSlide() {
  clearTimeout(timeoutId);
  const current = document.querySelector(".slide-img.active");
  const [next, prev] = getNextPrev();

  if (current.classList.contains("s-top")) {
    return;
  }

  prev.classList.add("s-top");
  current.classList.add("s-top");
  current.classList.remove("active");
  current.style.transform = "translate(100%)";
  prev.style.transform = "translate(0%)";
  prev.classList.add("active");

  getPosition();
  getActiveDots();
  autoLoop();
  console.log("getting the previous slide  ");
}

// dots
slides.forEach((slide) => {
  const dot = document.createElement("div");
  dot.classList.add("dot");
  dotEl.appendChild(dot);
});

function getActiveDots() {
  const allDots = document.querySelectorAll(".slide-dots .dot");
  const activeSlide = document.querySelector(".slide-img.active");
  const activeIndex = slides.indexOf(activeSlide);

  allDots.forEach((dot) => {
    dot.classList.remove("active");
  });

  allDots[activeIndex].classList.add("active");
}

function functionalDots() {
  const allDots = document.querySelectorAll(".slide-dots .dot");

  allDots.forEach((dot, index) => {
    dot.addEventListener("click", () => {
      getDotSlide(index);
    });
  });
}
function getDotSlide(index) {
  clearTimeout(timeoutId);
  slides.forEach((slide) => {
    slide.classList.remove("active");
  });
  slides[index].classList.add("active");
  getPosition();
  getActiveDots();
  autoLoop();
}
function autoLoop() {
  timeoutId = setTimeout(() => {
    getNextSlide();
  }, 5000);
}
functionalDots();
getActiveDots();
autoLoop();
