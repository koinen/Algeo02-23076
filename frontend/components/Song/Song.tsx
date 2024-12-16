import React, { useState, useEffect } from "react";
import * as Tone from "tone";
import { Midi } from "@tonejs/midi";
import { Card, CardContent, CardTitle } from "@/components/ui/card";
import Image from "next/image";
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card";
import { PlayIcon, StopIcon } from "@heroicons/react/solid";

export interface SongProps {
  fileName: string;
  mapping: {
    artist?: string;
    title?: string;
    image?: string;
  };
}

interface DisplayProps {
  song: SongProps;
  index: number;
}

const Song: React.FC<DisplayProps> = ({ song, index }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [midiData, setMidiData] = useState<any>(null);
  const songMapping = song.mapping || {
    artist: "Anonymous",
    title: "Untitled",
    image: "def.png",
  };
  
  useEffect(() => {
    // Load and parse MIDI file
    const loadMidi = async () => {
      const midiUrl = `/extracted/${song.fileName}`;
      const midi = await fetch(midiUrl)
        .then((response) => response.arrayBuffer())
        .then((buffer) => new Midi(buffer));

      setMidiData(midi);
    };

    loadMidi();
  }, [song.fileName]);

  const handleMidiPlayback = () => {
    if (isPlaying) {
      setIsPlaying(false);
      Tone.Transport.stop();
      Tone.Transport.cancel(); // Stop the transport and clear scheduled events
    } else {
      setIsPlaying(true);
      if (midiData) {
        // Set up Tone.js transport
        Tone.Transport.cancel(); // Clear any previous scheduled events

        // Iterate through each track in the MIDI file
        midiData.tracks.forEach((track: any) => {
          const synth = new Tone.Synth().toDestination();

          // Map through the notes in the track and schedule them for playback
          track.notes.forEach((note: any) => {
            synth.triggerAttackRelease(
              Tone.Frequency(note.midi, "midi").toFrequency(),
              note.duration,
              Tone.Transport.seconds + note.time
            );
          });
        });
        // Start the Tone.js transport to play the scheduled notes
        Tone.Transport.start();
      }
    }
  };

  let imagePath = "";
  if (songMapping.image === "def.png") {
    imagePath = `/album/def.png`;
  } else {
    imagePath = `/extracted/${songMapping.image}`;
  }

  return (
    <HoverCard>
      <HoverCardTrigger asChild>
        <Card className="p-4 h-fit bg-inherit">
          <CardContent className="flex flex-col justify-center items-center">
            <p className="text-2xl text-white">{index + 1}</p>
            <br />
            <Image
              className="border-4 border-solid border-black"
              src={imagePath}
              alt={"Not Found"}
              width={283}
              height={100}
            ></Image>
            <br />
            {song.fileName && song.fileName.toString().endsWith(".mid") ? (
              <button
                onClick={handleMidiPlayback}
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
              >
                {isPlaying ? (
                  <StopIcon className="h-5 w-5 text-white" />
                ) : (
                  <PlayIcon className="h-5 w-5 text-white" />
                )}
              </button>
            ) : (
              <audio src={`/extracted/${song.fileName}`} controls />
            )}
            <br />
            <CardTitle className="w-full overflow-hidden whitespace-nowrap text-ellipsis">
              <p className="text-3xl">{songMapping.title}</p>
            </CardTitle>
          </CardContent>
        </Card>
      </HoverCardTrigger>
      <HoverCardContent className="w-80">
        <div className="flex justify-between space-x-4">
          <div className="space-y-1">
            <p className="text-sm">Artist : {songMapping.artist}</p>
            <p className="text-sm">File Name : {song.fileName}</p>
          </div>
        </div>
      </HoverCardContent>
    </HoverCard>
  );
};

export default Song;
