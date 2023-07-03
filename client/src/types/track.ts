export type Track = {
  name: string;
  id: string;
};

export type FullTrack = {
  name: string;
  id: string;
  album: string;
  artists: string[];
  album_img_url: string;
};
