from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
import requests
from .models import MusicCategory, Song
from .forms import MusicCategoryForm, SongForm
from django.http import JsonResponse
from django.db import transaction

LASTFM_API_KEY = '1a305b4002e52baea744a7817f60701d'

@login_required
def add_category(request):
    if request.method == 'POST':
        form = MusicCategoryForm(request.POST)
        if form.is_valid():
            try:
                category = form.save(commit=False)
                category.user = request.user
                category.save()
                messages.success(request, "Category created successfully.")
                return redirect('dashboard')
            except Exception as e:
                print(f"Error saving category: {e}")
                form.add_error(None, "An error occurred while saving the category.")
    else:
        form = MusicCategoryForm()
    return render(request, 'music/add_category.html', {'form': form})

@login_required
def edit_category(request, category_id):
    if request.method == 'POST':
        category = get_object_or_404(MusicCategory, id=category_id, user=request.user)
        new_name = request.POST.get('new_name')

        if new_name:
            category.name = new_name
            category.save()
            messages.success(request, 'Category updated successfully.')
        else:
            messages.error(request, 'Category name cannot be empty.')

    return redirect('dashboard')

@login_required
def category_detail(request, category_id):
    print(f"Category ID: {category_id}")
    try:
        category = get_object_or_404(MusicCategory, id=category_id, user=request.user)
        print(f"Category: {category}")

        songs = category.songs.all()
        print(f"Songs: {songs}")

    except PermissionDenied:
        print("Permission Denied.")
        return redirect('dashboard')
    except Exception as e:
        print(f"Exception: {e}")
        messages.error(request, "Error fetching category details.")
        return redirect('dashboard')

    return render(request, 'music/category_detail.html', {
        'category': category,
        'songs': songs
    })
    
@login_required
def search_song(request):
    query = request.GET.get('query', '')
    results = []
    if query:
        try:
            results = search_song_api(query)
        except Exception as e:
            print(f"Error searching for songs: {e}")
            results = []
            messages.error(request, "An error occurred while searching for songs.")
    
    return render(request, 'music/search_results.html', {
        'results': results,
    })


@login_required
def add_song_to_category(request):
    try:
        if request.method == 'POST':
            form = SongForm(request.POST, request.FILES, user=request.user)

            if form.is_valid():
                title = form.cleaned_data.get('title')
                artist = form.cleaned_data.get('artist')
                category_id = form.cleaned_data.get('category').id
                audio_file = request.FILES.get('audio_file')

                # Validate that an audio file is provided
                if not audio_file:
                    error_message = "Please upload an audio file."
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        return JsonResponse({'success': False, 'message': error_message})
                    messages.error(request, error_message)
                    return redirect('add_song_to_category')

                category = get_object_or_404(MusicCategory, id=category_id, user=request.user)

                # Validate title and artist
                if not title or not artist:
                    error_message = "Please provide both the song title and the artist name."
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        return JsonResponse({'success': False, 'message': error_message})
                    messages.error(request, error_message)
                    return redirect('add_song_to_category')

                # Use transaction.atomic to ensure database integrity
                with transaction.atomic():
                    Song.objects.create(
                        category=category,
                        title=title,
                        artist=artist,
                        audio_file=audio_file
                    )
                
                success_message = "Song saved successfully."
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'message': success_message})
                messages.success(request, success_message)
                return redirect('dashboard')

            else:
                error_message = "Please correct the errors below."
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'errors': form.errors})
                messages.error(request, error_message)

        else:
            form = SongForm(user=request.user)

        categories = MusicCategory.objects.filter(user=request.user)

        context = {
            'form': form,
            'categories': categories
        }

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            print("AJAX request detected.")
            return render(request, 'music/add_song.html', context)
    except Exception as e:
        print(f"Error occurred: {e}")
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': "An unexpected error occurred."})
        messages.error(request, "An unexpected error occurred. Please try again.")
        return redirect('add_song_to_category')

def search_song_api(query):
    url = "https://ws.audioscrobbler.com/2.0/"
    params = {
        'method': 'track.search',
        'track': query,
        'api_key': LASTFM_API_KEY,
        'format': 'json',
        'limit': 10
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        data = response.json()

        # Safely extract the list of tracks
        results = data.get('results', {})
        trackmatches = results.get('trackmatches', {})
        tracks = trackmatches.get('track', [])

        # Process and return track information
        return [{
            'title': track.get('name', 'N/A'),
            'artist': track.get('artist', 'N/A'),
            'lastfm_url': track.get('url', None),
        } for track in tracks]

    except requests.RequestException as e:
        print(f"Error fetching song data: {e}")
        return []

@login_required
def delete_song(request, song_id):
    try:
        song = get_object_or_404(Song, id=song_id)
        if request.method == 'POST':
            song.delete()
            messages.success(request, 'Song deleted successfully.')
            # Redirect to the referring page or fallback to category detail page
            return redirect(request.META.get('HTTP_REFERER', 'dashboard'))
    except Exception as e:
        # Log the exception or handle it appropriately
        messages.error(request, 'An error occurred while trying to delete the song.')
        # Redirect to the dashboard or another page in case of error
        return redirect('dashboard')
    
    # Fallback in case of a non-POST request
    return redirect('dashboard')
