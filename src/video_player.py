"""A video player class."""

from .video_library import VideoLibrary
from .video_playlist import Playlist
import numpy as np
import random

class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self.playing = [False, ""]
        self.pause = False
        self.playlists = []

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        all_videos = self._video_library.get_all_videos()
        sorted_array = []
        for x in all_videos:
            sorted_array.append(x.title)
        sorted_array = np.sort(sorted_array)
        output_array = []
        for x in sorted_array:
            for y in all_videos:
                if x == y.title:
                    tag_list = list(y.tags)
                    tag_string = ""
                    for t in tag_list:
                        tag_string += f"{t} "
                    if y.flag == "":
                        output_array.append(f"  {x} ({y.video_id}) [{tag_string.strip()}]")
                    else:
                        output_array.append(f"  {x} ({y.video_id}) [{tag_string.strip()}] - FLAGGED (reason: {y.flag})")
        print("Here's a list of all available videos:")
        for x in output_array:
            print(x)

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        found = False
        self.pause = False
        all_videos = self._video_library.get_all_videos()
        for x in all_videos:
            if x.video_id == video_id:
                if x.flag != "":
                    print(f"Cannot play video: Video is currently flagged (reason: {x.flag})")
                    found = True
                else:
                    if self.playing[0] == True:
                        print(f"Stopping video: {self.playing[1]}")
                    print(f"Playing video: {x.title}")
                    self.playing = [True, x.title]
                    found = True
        if found == False:
            print("Cannot play video: Video does not exist")


    def stop_video(self):
        """Stops the current video."""
        if self.playing[0] == True:
            print(f"Stopping video: {self.playing[1]}")
            self.playing = [False, ""]
            self.pause = False
        else:
            print(f"Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""
        available_videos = []
        for x in self._video_library.get_all_videos():
            if x.flag == "":
                available_videos.append(x)
        if available_videos == []:
            print("No videos available")
        else:
            rand_index = random.randint(0,len(available_videos)-1)
            rand_id = available_videos[rand_index].video_id
            self.play_video(rand_id)

    def pause_video(self):
        """Pauses the current video."""
        if self.playing[0] == False:
            print("Cannot pause video: No video is currently playing")
        elif self.pause == True:
            print(f"Video already paused: {self.playing[1]}")
        else:
            print(f"Pausing video: {self.playing[1]}")
            self.pause = True

    def continue_video(self):
        """Resumes playing the current video."""
        if self.playing[0] == False:
            print("Cannot continue video: No video is currently playing")
        elif self.pause == False:
            print("Cannot continue video: Video is not paused")
        else:
            print(f"Continuing video: {self.playing[1]}")
            self.pause = False

    def show_playing(self):
        """Displays video currently playing."""
        if self.playing[0] == False:
            print ("No video is currently playing")
        else:
            output_str = ""
            for x in self._video_library.get_all_videos():
                if self.playing[1] == x.title:
                    tag_list = list(x.tags)
                    tag_string = ""
                    for t in tag_list:
                        tag_string += f"{t} "
                    output_str += f"{x.title} ({x.video_id}) [{tag_string.strip()}]"
            if self.pause == True:
                print(f"Currently playing: {output_str} - PAUSED")
            else:
                print(f"Currently playing: {output_str}")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        duplicate_check = False
        for x in self.playlists:
            if x.name.upper() == playlist_name.upper():
                duplicate_check = True
        if duplicate_check:
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            self.playlists.append(Playlist(playlist_name))
            print(f"Successfully created new playlist: {playlist_name}")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        video_find = [False]
        playlist_find = False
        for x in self.playlists:
            if x.name.upper() == playlist_name.upper():
                playlist_find = True
        for x in self._video_library.get_all_videos():
            if video_id == x.video_id:
                video_find.append([x.title, x.video_id,x.flag])
                video_find[0] = True
        if playlist_find == False:
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")
        elif video_find[0] == False:
            print(f"Cannot add video to {playlist_name}: Video does not exist")
        else:
            for x in self.playlists:
                if x.name.upper() == playlist_name.upper():
                    if video_find[1][2] != "":
                        print(f"Cannot add video to {playlist_name}: Video is currently flagged (reason: {video_find[1][2]})")
                    elif video_find[1][0] in x.videos:
                        print(f"Cannot add video to {playlist_name}: Video already added")
                    else:
                        x.videos.append(video_find[1][0])
                        print(f"Added video to {playlist_name}: {video_find[1][0]}")

    def show_all_playlists(self):
        """Display all playlists."""
        if self.playlists == []:
            print("No playlists exist yet")
        else:
            sorted_list = []
            for x in self.playlists:
                sorted_list.append(x.name)
            print("Showing all playlists:")
            for x in np.sort(sorted_list):
                print(f"    {x}")

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist_names = []
        for x in self.playlists:
            playlist_names.append(x.name.upper())
        if playlist_name.upper() not in playlist_names:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")
        else:
            all_videos = self._video_library.get_all_videos()
            for x in self.playlists:
                if x.name.upper() == playlist_name.upper():
                    print(f"Showing playlist: {playlist_name}")
                    if x.videos == []:
                        print("No videos here yet")
                    else:
                        for y in x.videos:
                            for z in all_videos:
                                if y == z.title:
                                    tag_list = list(z.tags)
                                    tag_string = ""
                                    for t in tag_list:
                                        tag_string += f"{t} "
                                    if z.flag == "":
                                        print(f"    {z.title} ({z.video_id}) [{tag_string.strip()}]")
                                    else:
                                        print(f"    {z.title} ({z.video_id}) [{tag_string.strip()}] - FLAGGED (reason: {z.flag})")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        playlists = []
        all_videos = self._video_library.get_all_videos()
        for x in self.playlists:
            playlists.append(x.name.upper())
        if playlist_name.upper() not in playlists:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
        else:
            for x in self.playlists:
                if playlist_name.upper() == x.name.upper():
                    videos = []
                    video_name = ""
                    for y in x.videos:
                        videos.append(y)
                    for y in all_videos:
                        if y.video_id == video_id:
                            video_name = y.title 
                    if video_name == "":
                        print(f"Cannot remove video from {playlist_name}: Video does not exist")
                    else:
                        if video_name in videos:
                            print(f"Removed video from {playlist_name}: {video_name}")
                            x.videos.remove(video_name)
                        else: 
                            print(f"Cannot remove video from {playlist_name}: Video is not in playlist")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        find = False
        for x in self.playlists:
            if playlist_name.upper() == x.name.upper():
                x.videos = []
                print(f"Successfully removed all videos from {playlist_name}")
                find = True
        if find == False:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")

        

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        find = False
        for x in self.playlists:
            if playlist_name.upper() == x.name.upper():
                self.playlists.remove(x)
                print(f"Deleted playlist: {playlist_name}")
                find = True
        if find == False:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")


    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """

        all_videos = self._video_library.get_all_videos()
        results = []
        results_name = []
        for x in all_videos:
            if search_term.upper() in x.title.upper():
                results.append(x)
        if results == []:
            print(f"No search results for {search_term}")
        else:
            for x in results:
                results_name.append(x.title)
            results_name = np.sort(results_name)
            results_sorted = []
            for x in results_name:
                for y in results:
                    if x == y.title:
                        tag_list = list(y.tags)
                        tag_string = ""
                        for t in tag_list:
                            tag_string += f"{t} "
                        if y.flag == "":
                            results_sorted.append([y.title, y.video_id, tag_string.strip()])
            i = 1
            print(f"Here are the results for {search_term}:")
            for x in results_sorted:
                print(f"{i}) {x[0]} ({x[1]}) [{x[2]}]")
                i += 1
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            response = input()
            if response.isnumeric():
                index = int(response) - 1
                if index < len(results_sorted):
                    self.play_video(results_sorted[index][1])

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        all_videos = self._video_library.get_all_videos()
        results = []
        results_name = []
        for x in all_videos:
            tag_list = list(x.tags)
            tag_string = ""
            for t in tag_list:
                tag_string += f"{t} "
            if video_tag.upper() in tag_string.upper():
                if x.flag == "":
                    results.append([x.title, x.video_id, tag_string.strip()])
        if (results == []) | (video_tag[0] != "#"):
            print(f"No search results for {video_tag}")
        else:
            for x in results:
                results_name.append(x[0])
            results_name = np.sort(results_name)
            results_sorted = []
            for x in results_name:
                for y in results:
                    if x == y[0]:
                        results_sorted.append(y)
            i = 1
            print(f"Here are the results for {video_tag}:")
            for x in results_sorted:
                print(f"{i}) {x[0]} ({x[1]}) [{x[2]}]")
                i += 1
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            response = input()
            if response.isnumeric():
                index = int(response) - 1
                if index < len(results_sorted):
                    self.play_video(results_sorted[index][1])


    def flag_video(self, video_id, flag_reason = "Not supplied"):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        all_videos = self._video_library.get_all_videos()
        found = [False]
        for x in all_videos:
            if x.video_id == video_id:
                found.append([x.title, x.video_id, x.tags, x.flag])
                found[0] = True
        if found[0] == False:
            print("Cannot flag video: Video does not exist")
        elif found[1][3] != "":
                print(f"Cannot flag video: Video is already flagged (reason: {found[1][3]})")
        else:
            if self.playing[0] == True:
                if self.playing[1] == found[1][0]:
                    self.stop_video()
            print(f"Successfully flagged video: {found[1][0]} (reason: {flag_reason})")
            for x in self._video_library.get_all_videos():
                if x.video_id == video_id:
                    x.change_flag(flag_reason)



    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        find = self._video_library.get_video(video_id)
        if find == None:
            print("Cannot remove flag from video: Video does not exist")
        elif find.flag == "":
            print("Cannot remove flag from video: Video is not flagged")
        else:
            find.change_flag("")
            print(f"Successfully removed flag from video: {find.title}")
cd ..