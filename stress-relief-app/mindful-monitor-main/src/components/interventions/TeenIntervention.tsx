import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { CheckCircle2, Save } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

interface TeenInterventionProps {
  onClose: () => void;
}

const feelings = [
  { emoji: "😰", label: "Anxious" },
  { emoji: "😢", label: "Sad" },
  { emoji: "😤", label: "Frustrated" },
  { emoji: "😴", label: "Tired" },
  { emoji: "😨", label: "Overwhelmed" },
  { emoji: "😶", label: "Numb" },
  { emoji: "🤔", label: "Confused" },
  { emoji: "😠", label: "Angry" },
  { emoji: "😖", label: "Stressed" },
];

const triggers = [
  "School/Work", "Relationships", "Family", "Health", 
  "Money", "Future", "Social Media", "Other"
];

const TeenIntervention = ({ onClose }: TeenInterventionProps) => {
  const { toast } = useToast();
  const [selectedFeelings, setSelectedFeelings] = useState<string[]>([]);
  const [selectedTriggers, setSelectedTriggers] = useState<string[]>([]);
  const [notes, setNotes] = useState("");
  const [aiPrompt, setAiPrompt] = useState("");
  const [savedEntry, setSavedEntry] = useState(false);

  const toggleFeeling = (feeling: string) => {
    setSelectedFeelings(prev =>
      prev.includes(feeling)
        ? prev.filter(f => f !== feeling)
        : [...prev, feeling]
    );
  };

  const toggleTrigger = (trigger: string) => {
    setSelectedTriggers(prev =>
      prev.includes(trigger)
        ? prev.filter(t => t !== trigger)
        : [...prev, trigger]
    );
  };

  const saveJournal = () => {
    // Simulate saving and generating AI prompt
    setSavedEntry(true);
    const prompts = [
      "What small step could you take today to ease one of these feelings?",
      "When have you felt this way before, and what helped?",
      "Who in your life could you reach out to about this?",
      "What would you tell a friend who felt this way?",
    ];
    setAiPrompt(prompts[Math.floor(Math.random() * prompts.length)]);
    
    toast({
      title: "Journal saved",
      description: "Your entry has been saved securely.",
    });
  };

  return (
    <Card className="border-l-4 border-l-teen-accent bg-card shadow-lg">
      <div className="p-6">
        {/* Header */}
        <div className="mb-6">
          <h2 className="text-2xl font-semibold text-foreground mb-2">
            Hey, looks like you could use a break 💙
          </h2>
        </div>

        {/* Tabs */}
        <Tabs defaultValue="journal" className="w-full">
          <TabsList className="grid w-full grid-cols-4 mb-6">
            <TabsTrigger value="reading">📖 Reading</TabsTrigger>
            <TabsTrigger value="art">🎨 Art</TabsTrigger>
            <TabsTrigger value="meditation">🧘 Meditation</TabsTrigger>
            <TabsTrigger value="journal">📝 Journal</TabsTrigger>
          </TabsList>

          <TabsContent value="reading" className="space-y-4">
            <Card className="p-6 bg-muted">
              <p className="text-lg leading-relaxed">
                Mindfulness reading content will be generated here. Focus on the present moment, 
                your breath, and remember that this feeling is temporary.
              </p>
            </Card>
          </TabsContent>

          <TabsContent value="art" className="space-y-4">
            <div className="aspect-video bg-muted rounded-lg flex items-center justify-center">
              <p className="text-muted-foreground">Art therapy video placeholder</p>
            </div>
          </TabsContent>

          <TabsContent value="meditation" className="space-y-4">
            <Card className="p-6 bg-muted text-center">
              <div className="text-5xl mb-4">🧘</div>
              <p className="text-lg mb-4">5-minute guided meditation</p>
              <Button className="w-full h-12">▶️ Start Meditation</Button>
            </Card>
          </TabsContent>

          <TabsContent value="journal" className="space-y-6">
            {/* Feelings */}
            <div>
              <h3 className="text-lg font-semibold mb-3">How are you feeling?</h3>
              <div className="grid grid-cols-3 gap-3">
                {feelings.map((feeling) => (
                  <Button
                    key={feeling.label}
                    variant={selectedFeelings.includes(feeling.label) ? "default" : "outline"}
                    className="h-auto py-3 flex flex-col gap-2"
                    onClick={() => toggleFeeling(feeling.label)}
                  >
                    <span className="text-2xl">{feeling.emoji}</span>
                    <span className="text-sm">{feeling.label}</span>
                  </Button>
                ))}
              </div>
            </div>

            {/* Triggers */}
            <div>
              <h3 className="text-lg font-semibold mb-3">What's on your mind?</h3>
              <div className="flex flex-wrap gap-2">
                {triggers.map((trigger) => (
                  <Badge
                    key={trigger}
                    variant={selectedTriggers.includes(trigger) ? "default" : "outline"}
                    className="cursor-pointer px-4 py-2 text-sm"
                    onClick={() => toggleTrigger(trigger)}
                  >
                    {trigger}
                  </Badge>
                ))}
              </div>
            </div>

            {/* Notes */}
            <div>
              <h3 className="text-lg font-semibold mb-3">Any other thoughts?</h3>
              <Textarea
                placeholder="Optional: Share what's on your mind..."
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                className="min-h-32"
              />
            </div>

            {/* Save Button */}
            {!savedEntry ? (
              <Button
                onClick={saveJournal}
                className="w-full h-12 text-lg bg-teen-accent hover:bg-teen-accent/90"
              >
                <Save className="mr-2 h-5 w-5" />
                💾 Save Journal Entry
              </Button>
            ) : (
              <>
                <Card className="p-4 bg-teen-bg border-teen-accent">
                  <div className="flex items-start gap-3">
                    <span className="text-2xl">💭</span>
                    <div>
                      <p className="font-semibold mb-2">Reflection Prompt:</p>
                      <p className="text-foreground/90">{aiPrompt}</p>
                    </div>
                  </div>
                </Card>

                <Button
                  onClick={onClose}
                  variant="outline"
                  className="w-full h-12 text-lg"
                >
                  <CheckCircle2 className="mr-2 h-5 w-5" />
                  Done
                </Button>
              </>
            )}
          </TabsContent>
        </Tabs>
      </div>
    </Card>
  );
};

export default TeenIntervention;
