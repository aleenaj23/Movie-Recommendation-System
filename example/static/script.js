$(document).ready(function() {
  console.log("hi");
  $('.fail').css('display','none');
  $(".loader").css('display', 'none');
  $('#movie-name').on('input', function() {
    var query = $(this).val();
    if (query.length > 1) {
        $.ajax({
            type: 'GET',
            url: '/autocomplete',
            data: {query: query},
            success: function(data) {
                $('#autocomplete-list').empty();
                $.each(data, function(index, title) {
                    $('#autocomplete-list').append('<li>' + title + '</li>');
                });
                $('#autocomplete-list').show();
            }
        });
    } else {
        $('#autocomplete-list').hide();
    }
  });

  $(document).on('click', function(event) {
      if ($(event.target).closest('#movie-name, #autocomplete-list').length === 0) {
          $('#autocomplete-list').hide();
      }
  });

  $('#autocomplete-list').on('click', 'li', function() {
      $('#movie-name').val($(this).text());
      $('#autocomplete-list').hide();
  });

});


// $(function() {
//   $('#startButton').on('click', function(){
//     window.location.href = '/loadlang';
//   });
// });





function recommendcard(e){
  var my_api_key = '64f14bfc62f718d2cf962fe150e5bc40';
  var title = e.getAttribute('title'); 
  load_details(my_api_key,title, true);
}

///////////////////////////////////

$(function(){
  $('#startButton').on('click', function(){
    window.location.href = '/loadlang';
  });
})
// $(function() {
 
//   $('.flip-card-inner').on('click', function() {
//     var filteringText = $(this).attr('id'); 
//     console.log(filteringText)
//     if (filteringText === "filtering"){
//       window.location.href = '/filter';
//     }
//     else if (filteringText === "recommendation"){
//       window.location.href = '/index'
//     }
//   });
// });


$(function() {
  $('.language-option').on('click', function() {
    var language = $(this).attr('id'); 
    window.location.href = '/preference?lang=' + language;

  });
});

//////////////////////////////////


////navigations

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

//function when movie title is submitted
$(function() {
    $('#submit-button').on('click', function(){
    
    var title = $('#movie-name').val().toLowerCase();
    $('#movie-name').val('');
    var my_api_key = '64f14bfc62f718d2cf962fe150e5bc40';
    console.log(title);
    load_details(my_api_key, title, true);
    });
});

//loading details of the current selected movie
function load_details(my_api_key,search,isQuerySearch){
    if(isQuerySearch) {
      $("#loader").fadeIn();
      url = 'https://api.themoviedb.org/3/search/movie?api_key='+my_api_key+'&query='+search;
    }
    else {
      url = 'https://api.themoviedb.org/3/movie/' + search + '?api_key='+my_api_key;
    }
   
    $.ajax({
      type: 'GET',
      url:url,
      async: false,
      success: function(movie){
        //Implement:  load details function to handle if no results are found should be added. ******************************
        if(movie.results.length==1) {
          var movie_id = movie.results[0].id;
          var movie_title = movie.results[0].title;
          var movie_title_org = movie.results[0].original_title;
          console.log(movie_id, movie_title, movie_title_org);
          get_recommendations(movie_title, movie_id, my_api_key, movie_title_org);
        }
        else if(movie.results.length > 1){
  // Implement : when multiple results are found just pass the title to the python flask, it will return the imdb id then fetch details using omdb api
          // var details = {
          //   'movies_list': movie.results
          // }

          $.ajax({
            type: 'POST',
            data:{'title':search},  
            url:"/findmalayalam",
            success: function(movie){
              console.log(movie);
              var movie_id = movie.movie_results[0].id;
              var movie_title = movie.movie_results[0].title;
              var movie_title_org = movie.movie_results[0].original_title;
              console.log(movie_id, movie_title, movie_title_org);
              get_recommendations(movie_title, movie_id, my_api_key, movie_title_org);
              
             }
          });
        }
      },
    });
  }
  
  function get_recommendations(movie_title, movie_id, my_api_key, movie_title_org){
    rec_movies = [];
    rec_posters = [];
    
    rec_ids = [];

    $.ajax({
      type:'POST',
      url:"/similarity_movie",
      data:{'name':movie_title},
      success: function(recs){
        if(recs==="Sorry! The movie you requested is not in our database. Please check the spelling or try with some other movies"){
          // code for displaying fail condition have to be included in the html code.
          // $('.fail').css('display','block');
          // $('.results').css('display','none');
          $("#loader").delay(500).fadeOut();
          console.log(recs);
        }
        else {
          // $('.fail').css('display','none');
          // $('.results').css('display','block');
          console.log(recs);
          for(movie in recs){
            rec_ids.push(recs[movie].imdb_id)
            rec_movies.push(recs[movie].Title)
          }
          // var movie_arr = recs.split('---');
          // var arr = [];
          // for(const movie in movie_arr){
          //   arr.push(movie_arr[movie]);
          //   rec_movies.push(movie_arr[movie]);
          // }
          console.log(rec_movies);
          console.log(rec_ids);
          get_movie_details(movie_id, my_api_key, rec_movies,rec_ids, movie_title,movie_title_org)
        }
      },
      error: function(){
        alert("error recs");
        $("#loader").delay(500).fadeOut();
      },
    }); 
  
  }

function get_movie_details(movie_id, my_api_key, rec_movies, rec_ids, movie_title,movie_title_org){
  $.ajax({
    type:'GET',
    url:'https://api.themoviedb.org/3/movie/'+movie_id+'?api_key='+my_api_key,
    success: function(movie_details){
      show_details(movie_details,movie_title,my_api_key,rec_movies,rec_ids, movie_id,movie_title_org);
    },
    error: function(error){
      alert("API Error! - "+error);
      // $("#loader").delay(500).fadeOut();
    },
  });
}

function show_details(movie_details,movie_title,my_api_key,rec_movies,rec_ids, movie_id,movie_title_org){
  var imdb_id = movie_details.imdb_id;
  var poster;
  if(movie_details.poster_path){
    poster = 'https://image.tmdb.org/t/p/original'+movie_details.poster_path;
  }
  else {
    poster = 'static/default.jpg';
  }
  var overview = movie_details.overview;
  var genres = movie_details.genres;
  var rating = movie_details.vote_average;
  var vote_count = movie_details.vote_count;
  var release_date = movie_details.release_date;
  var runtime = parseInt(movie_details.runtime);
  var status = movie_details.status;
  var genre_list = []
  for (var genre in genres){
    genre_list.push(genres[genre].name);
  }
  var my_genre = genre_list.join(", ");
  if(runtime%60==0){
    runtime = Math.floor(runtime/60)+" hour(s)"
  }
  else {
    runtime = Math.floor(runtime/60)+" hour(s) "+(runtime%60)+" min(s)"
  }
   
  // rec_posters = get_movie_posters(rec_ids, my_api_key) // *****************************************

  // calling `get_movie_cast` to get the top cast for the queried movie
  movie_cast = get_movie_cast(movie_id,my_api_key);
  
  // calling `get_individual_cast` to get the individual cast details
  ind_cast = get_individual_cast(movie_cast,my_api_key);
  
  details = {
      'title':movie_title,
      'orginal_title' : movie_title_org,
      'cast_ids':JSON.stringify(movie_cast.cast_ids),
      'cast_names':JSON.stringify(movie_cast.cast_names),
      'cast_chars':JSON.stringify(movie_cast.cast_chars),
      'cast_profiles':JSON.stringify(movie_cast.cast_profiles),
      'cast_bdays':JSON.stringify(ind_cast.cast_bdays),
      'cast_bios':JSON.stringify(ind_cast.cast_bios),
      'cast_places':JSON.stringify(ind_cast.cast_places),
      'imdb_id':imdb_id,
      'poster':poster,
      'genres':my_genre,
      'overview':overview,
      'rating':rating,
      'vote_count':vote_count.toLocaleString(),
      'rel_date':release_date,  
      'release_date':new Date(release_date).toDateString().split(' ').slice(1).join(' '),
      'runtime':runtime,
      'status':status,
      'rec_movies':JSON.stringify(rec_movies),
      // 'rec_posters':JSON.stringify(rec_posters),
      'rec_ids' : JSON.stringify(rec_ids),
  }

  $.ajax({
    type:'POST',
    data:details,
    url:"/recommend",
    dataType: 'html',
    success: function(response) {
      $('.results').html(response);
      $('#autoComplete').val('');
      $('.footer').css('position','absolute');
      // if ($('.movie-content')) {
      //   $('.movie-content').after('<div class="gototop"><i title="Go to Top" class="fa fa-arrow-up"></i></div>');
      // }
      $(window).scrollTop(0);
    }
  });
}

function get_movie_posters(arr,my_api_key){
  var arr_poster_list = []
  for(var m in arr) {
    $.ajax({
      type:'GET',
      // url:'https://api.themoviedb.org/3/search/movie?api_key='+my_api_key+'&query='+arr[m],
      url: 'https://api.themoviedb.org/3/find/'+arr[m]+'?api_key='+my_api_key+'&external_source=imdb_id',
      async: false,
      success: function(m_data){
        if (m_data.movie_results[0].poster_path){
          arr_poster_list.push('https://image.tmdb.org/t/p/original'+m_data.movie_results[0].poster_path);
        }
        else{
          arr_poster_list.push('static/movie_placeholder.jpeg');
        }
      },
      error: function(){
        alert("Invalid Request!");
        // $("#loader").delay(500).fadeOut();
      },
    })
  }
  return arr_poster_list;
}


// get the details of individual cast
function get_individual_cast(movie_cast,my_api_key) {
  cast_bdays = [];
  cast_bios = [];
  cast_places = [];
  for(var cast_id in movie_cast.cast_ids){
    $.ajax({
      type:'GET',
      url:'https://api.themoviedb.org/3/person/'+movie_cast.cast_ids[cast_id]+'?api_key='+my_api_key,
      async:false,
      success: function(cast_details){
        cast_bdays.push((new Date(cast_details.birthday)).toDateString().split(' ').slice(1).join(' '));
        cast_bios.push(cast_details.biography);
        cast_places.push(cast_details.place_of_birth);
      }
    });
  }
  return {cast_bdays:cast_bdays,cast_bios:cast_bios,cast_places:cast_places};
}

// getting the details of the cast for the requested movie
function get_movie_cast(movie_id,my_api_key){
  cast_ids= [];
  cast_names = [];
  cast_chars = [];
  cast_profiles = [];

  top_10 = [0,1,2,3,4,5,6,7,8,9];
  $.ajax({
    type:'GET',
    url:"https://api.themoviedb.org/3/movie/"+movie_id+"/credits?api_key="+my_api_key,
    async:false,
    success: function(my_movie){
      if(my_movie.cast.length>=10){
        top_cast = [0,1,2,3,4,5,6,7,8,9];
      }
      else {
        top_cast = [0,1,2,3,4];
      }
      for(var my_cast in top_cast){
        cast_ids.push(my_movie.cast[my_cast].id)
        cast_names.push(my_movie.cast[my_cast].name);
        cast_chars.push(my_movie.cast[my_cast].character);
        if(my_movie.cast[my_cast].profile_path){
          cast_profiles.push("https://image.tmdb.org/t/p/original"+my_movie.cast[my_cast].profile_path);
        }
        else{
          cast_profiles.push("static/default.jpg");
        }
        
      }
    },
    error: function(){
      alert("Invalid Request!");
      // $("#loader").delay(500).fadeOut();
    }
  });

  return {cast_ids:cast_ids,cast_names:cast_names,cast_chars:cast_chars,cast_profiles:cast_profiles};
}
