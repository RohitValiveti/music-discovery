import React from "react";

type SongModalPropType = {
  id?: string | undefined;
  album?: string | undefined;
  name?: string | undefined;
  artists?: string[] | undefined;
  playlist_id: string | undefined;
};

const SongModal = ({
  id,
  album,
  name,
  artists,
  playlist_id,
}: SongModalPropType) => {
  return (
    <div>
      <h3>{name}</h3>
      <p>Album: {album}</p>
      {artists && (
        <p>
          Artist(s):{" "}
          {artists.map((artist) => (
            <p>{artist}</p>
          ))}
        </p>
      )}
      {/* <img src={require('/default.png')} alt="cover" /> */}
    </div>
  );
};

export default SongModal;
