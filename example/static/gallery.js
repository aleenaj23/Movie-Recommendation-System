const sections = document.querySelectorAll('.latest-releases');
const scrollAmount = 600; // Amount to scroll each time (in pixels)

sections.forEach(section => {
    const latestPosters = section.querySelector('.latest-posters');
    const scrollLeftButton = section.querySelector('.poster_scroll:first-child');
    const scrollRightButton = section.querySelector('.poster_scroll:last-child');

    scrollLeftButton.addEventListener('click', () => {
        latestPosters.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    });

    scrollRightButton.addEventListener('click', () => {
        latestPosters.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    });
});

$(function() {
    $('#home-tab').on('click', function() {
      window.location.href = '/';
    });
  });
  
  $(function() {
    $('#gallery-tab').on('click', function() {
      window.location.href = '/gallery';
    });
  });
  
  $(function() {
    $('#recommendation-tab').on('click', function() {
      window.location.href = '/loadlang';
    });
  });
  
  $(function() {
    $('#filter-tab').on('click', function() {
      window.location.href = '/filter';
    });
  });
  
  $(function() {
    $('#features-tab').on('click', function() {
      window.location.href = '/features';
    });
  });
  


// const latestPosters = document.querySelector('.latest-posters');
// const scrollLeftButton = document.querySelector('.poster_scroll:first-child');
// const scrollRightButton = document.querySelector('.poster_scroll:last-child');

// const scrollAmount = 600; // Amount to scroll each time (in pixels)

// scrollLeftButton.addEventListener('click', () => {
//     latestPosters.computedStyleMap.scrollBehavior = "smooth";
//     latestPosters.scrollLeft -= scrollAmount;
// });

// scrollRightButton.addEventListener('click', () => {
//     latestPosters.computedStyleMap.scrollBehavior = "smooth";
//     latestPosters.scrollLeft += scrollAmount;
// });