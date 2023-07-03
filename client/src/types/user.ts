import { Track } from "./track";

export type User = {
  followers: number;
  name: string;
  public_playlists: number;
  top_tracks: Track[];
  user_img_url: string;
};
