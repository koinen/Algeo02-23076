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
export interface SongProps {
  fileName: string;
  mapping: {
    artist?: string;
    title?: string;
    image?: string;
  };
}

const Song: React.FC<SongProps> = ({ fileName, mapping }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [midiData, setMidiData] = useState<any>(null);

  useEffect(() => {
    // Load and parse MIDI file
    const loadMidi = async () => {
      const midiUrl = `/extracted/${fileName}`;
      const midi = await fetch(midiUrl)
        .then((response) => response.arrayBuffer())
        .then((buffer) => new Midi(buffer));

      setMidiData(midi);
    };

    loadMidi();
  }, [fileName]);

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
  if (mapping?.image === "def.png") {
    imagePath = `/album/${mapping?.image}`;
  } else {
    imagePath = `/extracted/${mapping?.image}`;
  }

  return (
    <HoverCard>
      <HoverCardTrigger asChild>
        <Card className="p-4 h-fit bg-inherit">
          <CardContent className="flex flex-col justify-center items-center">
            <Image
              className="border-4 border-solid border-black"
              src={imagePath}
              alt={"Not Found"}
              width={283}
              height={100}
            ></Image>
            <br />
            {fileName.toString().endsWith(".mid") ? (
              <button
                onClick={handleMidiPlayback}
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
              >
                {isPlaying ? "Stop" : "Play"}
              </button>
            ) : (
              <audio src={`/extracted/${fileName}`} controls />
            )}
            <br />
            <CardTitle className="border-4 border-solid border-black w-full">
              {mapping?.title}
            </CardTitle>
          </CardContent>
        </Card>
      </HoverCardTrigger>
      <HoverCardContent className="w-80">
        <div className="flex justify-between space-x-4">
          <div className="space-y-1">
            <p className="text-sm">Artist : {mapping?.artist}</p>
            <p className="text-sm">File Name : {fileName}</p>
          </div>
        </div>
      </HoverCardContent>
    </HoverCard>
  );
};

export default Song;