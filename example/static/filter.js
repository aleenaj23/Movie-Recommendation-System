  
$(function(){
  $('.next_button').on('click', function(){
    console.log('next');
    display();
  });
});

function display(){
  const elem_a = document.querySelector('#actor_option').getDisplayValue();
  const elem_d = document.querySelector('#director_option').getDisplayValue();
  const elem_y = document.querySelector('#year_option').getDisplayValue();

  console.log( document.querySelector('#actor_option').getDisplayValue());
  console.log( document.querySelector('#director_option').getDisplayValue());

  actor = []
  director = []
  year = []

  for (const value in elem_a){
      actor.push(elem_a[value]);
  }

  for (const value in elem_d){
      director.push(elem_d[value]);
  }
  for (const value in elem_y){
      year.push(elem_y[value]);
  }
  details = {
    'actors' : JSON.stringify(actor),
    'directors' : JSON.stringify(director),
    'years' : JSON.stringify(year),
  }

  $.ajax({
    type:'POST',
    data:details,
    url:"/filtering",
    dataType: 'html',
    success: function(response) {
      $('.results').html(response);
    }
  });
  };

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
  