import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Sparkles, Volume2, CheckCircle2 } from "lucide-react";

interface ChildInterventionProps {
  onClose: () => void;
}

const ChildIntervention = ({ onClose }: ChildInterventionProps) => {
  const [story, setStory] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);

  const generateStory = () => {
    setIsGenerating(true);
    // Simulate story generation
    setTimeout(() => {
      setStory(
        "Once upon a time, in a magical forest filled with friendly animals, there lived a little bunny named Fluffy. " +
        "Fluffy loved to hop around and make new friends. One sunny day, Fluffy felt a bit worried about meeting new friends. " +
        "But then, a wise old owl told Fluffy a secret: 'When you feel worried, just take three deep breaths and think of something that makes you smile!' " +
        "Fluffy tried it, and it worked like magic! Soon, Fluffy was hopping happily and making lots of new friends. The end."
      );
      setIsGenerating(false);
    }, 2000);
  };

  const readAloud = () => {
    if ('speechSynthesis' in window && story) {
      const utterance = new SpeechSynthesisUtterance(story);
      utterance.rate = 0.9;
      utterance.pitch = 1.1;
      window.speechSynthesis.speak(utterance);
    }
  };

  return (
    <Card className="border-l-4 border-l-stressed bg-gradient-to-br from-yellow-50 to-orange-50 shadow-lg">
      <div className="p-6">
        {/* Header */}
        <div className="mb-6">
          <div className="text-5xl mb-2">😰</div>
          <h2 className="text-2xl font-bold text-foreground mb-2">
            You seem stressed! Let's try something fun!
          </h2>
        </div>

        {/* Tabs */}
        <Tabs defaultValue="story" className="w-full">
          <TabsList className="grid w-full grid-cols-2 mb-6">
            <TabsTrigger value="story" className="text-lg">
              📖 Story Time
            </TabsTrigger>
            <TabsTrigger value="activities" className="text-lg">
              🎨 Calm Activities
            </TabsTrigger>
          </TabsList>

          {/* Story Tab */}
          <TabsContent value="story" className="space-y-4">
            <Button
              onClick={generateStory}
              disabled={isGenerating}
              className="w-full h-14 text-lg bg-secondary hover:bg-secondary/90"
            >
              {isGenerating ? (
                <>
                  <span className="animate-spin mr-2">⏳</span>
                  Creating Your Story...
                </>
              ) : (
                <>
                  <Sparkles className="mr-2 h-5 w-5" />
                  Generate New Story
                </>
              )}
            </Button>

            {story && (
              <Card className="p-6 bg-card">
                <div className="prose prose-lg max-w-none">
                  <p className="text-xl leading-relaxed">{story}</p>
                </div>
                
                <Button
                  onClick={readAloud}
                  variant="outline"
                  className="w-full mt-4 h-12 text-lg"
                >
                  <Volume2 className="mr-2 h-5 w-5" />
                  🔊 Read Story Aloud
                </Button>
              </Card>
            )}
          </TabsContent>

          {/* Activities Tab */}
          <TabsContent value="activities" className="space-y-4">
            <div className="border-4 border-calm rounded-xl overflow-hidden">
              <div className="bg-calm text-calm-foreground p-3 text-center font-semibold">
                🎨 Follow Along: Guided Painting
              </div>
              <div className="aspect-video bg-muted flex items-center justify-center">
                <div className="text-center text-muted-foreground">
                  <div className="text-6xl mb-4">🎨</div>
                  <p>Calming painting video will play here</p>
                </div>
              </div>
            </div>
          </TabsContent>
        </Tabs>

        {/* Footer */}
        <Button
          onClick={onClose}
          className="w-full mt-6 h-14 text-lg bg-calm hover:bg-calm/90"
        >
          <CheckCircle2 className="mr-2 h-5 w-5" />
          ✅ I feel better now
        </Button>
      </div>
    </Card>
  );
};

export default ChildIntervention;
