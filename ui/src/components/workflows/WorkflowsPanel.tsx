import { useState } from 'react';
import { 
  Workflow, 
  Play, 
  Pause, 
  RotateCcw, 
  CheckCircle2, 
  XCircle,
  Clock,
  MoreHorizontal,
  Plus,
  GitBranch
} from 'lucide-react';
import { cn } from '@/lib/utils';

interface WorkflowDef {
  id: string;
  name: string;
  description: string;
  status: 'idle' | 'running' | 'completed' | 'failed';
  progress: number;
  steps: number;
  duration: string;
  lastRun: string;
}

const SAMPLE_WORKFLOWS: WorkflowDef[] = [
  {
    id: '1',
    name: 'Marketing Campaign Launch',
    description: 'Full campaign from content creation to distribution',
    status: 'running',
    progress: 65,
    steps: 8,
    duration: '12m 34s',
    lastRun: '2 min ago'
  },
  {
    id: '2',
    name: 'Product Feature Development',
    description: 'End-to-end feature implementation with QA',
    status: 'completed',
    progress: 100,
    steps: 12,
    duration: '45m 12s',
    lastRun: '1 hour ago'
  },
  {
    id: '3',
    name: 'Security Audit & Remediation',
    description: 'Automated security scan and fix deployment',
    status: 'idle',
    progress: 0,
    steps: 6,
    duration: '-',
    lastRun: 'Never'
  },
  {
    id: '4',
    name: 'Content Generation Pipeline',
    description: 'Auto-generate blog posts and social content',
    status: 'running',
    progress: 30,
    steps: 5,
    duration: '5m 20s',
    lastRun: 'Running'
  },
  {
    id: '5',
    name: 'Competitor Analysis Report',
    description: 'Research and analyze competitor activities',
    status: 'failed',
    progress: 45,
    steps: 4,
    duration: '8m 15s',
    lastRun: '3 hours ago'
  }
];

function WorkflowCard({ workflow }: { workflow: WorkflowDef }) {
  // Status colors defined but not used in this component

  const statusIcons = {
    idle: Clock,
    running: Play,
    completed: CheckCircle2,
    failed: XCircle
  };

  const StatusIcon = statusIcons[workflow.status];

  return (
    <div className="p-5 bg-card rounded-xl border border-border hover:border-primary/50 transition-all">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className={cn(
            "p-2 rounded-lg",
            workflow.status === 'running' ? 'bg-blue-500/20' : 'bg-accent'
          )}>
            <Workflow className={cn(
              "w-5 h-5",
              workflow.status === 'running' ? 'text-blue-500 animate-pulse' : 'text-muted-foreground'
            )} />
          </div>
          <div>
            <h3 className="font-semibold">{workflow.name}</h3>
            <p className="text-sm text-muted-foreground">{workflow.description}</p>
          </div>
        </div>
        <div className={cn(
          "flex items-center gap-2 px-3 py-1 rounded-full text-xs",
          workflow.status === 'running' ? 'bg-blue-500/20 text-blue-500' :
          workflow.status === 'completed' ? 'bg-green-500/20 text-green-500' :
          workflow.status === 'failed' ? 'bg-red-500/20 text-red-500' :
          'bg-gray-500/20 text-gray-500'
        )}>
          <StatusIcon className="w-3 h-3" />
          <span className="capitalize">{workflow.status}</span>
        </div>
      </div>

      {/* Progress */}
      <div className="mb-4">
        <div className="flex items-center justify-between text-xs mb-2">
          <span className="text-muted-foreground">Progress</span>
          <span className="font-medium">{workflow.progress}%</span>
        </div>
        <div className="h-2 bg-accent rounded-full overflow-hidden">
          <div 
            className={cn(
              "h-full rounded-full transition-all duration-500",
              workflow.status === 'running' ? 'bg-blue-500' :
              workflow.status === 'completed' ? 'bg-green-500' :
              workflow.status === 'failed' ? 'bg-red-500' :
              'bg-gray-500'
            )}
            style={{ width: `${workflow.progress}%` }}
          />
        </div>
      </div>

      {/* Stats */}
      <div className="flex items-center gap-6 text-sm text-muted-foreground mb-4">
        <span>{workflow.steps} steps</span>
        <span>Duration: {workflow.duration}</span>
        <span>Last run: {workflow.lastRun}</span>
      </div>

      {/* Actions */}
      <div className="flex items-center gap-2">
        {workflow.status === 'idle' && (
          <button className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors">
            <Play className="w-4 h-4" />
            Run
          </button>
        )}
        {workflow.status === 'running' && (
          <button className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-yellow-500/20 text-yellow-500 rounded-lg hover:bg-yellow-500/30 transition-colors">
            <Pause className="w-4 h-4" />
            Pause
          </button>
        )}
        {(workflow.status === 'completed' || workflow.status === 'failed') && (
          <button className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-accent hover:bg-accent/80 rounded-lg transition-colors">
            <RotateCcw className="w-4 h-4" />
            Rerun
          </button>
        )}
        <button className="p-2 hover:bg-accent rounded-lg transition-colors">
          <MoreHorizontal className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}

export function WorkflowsPanel() {
  const [view, setView] = useState<'grid' | 'flow'>('grid');

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Workflows</h2>
          <p className="text-muted-foreground">Orchestrate multi-agent operations</p>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex bg-card rounded-lg p-1 border border-border">
            <button
              onClick={() => setView('grid')}
              className={cn(
                "px-3 py-1.5 rounded-md text-sm transition-colors",
                view === 'grid' ? 'bg-primary text-primary-foreground' : 'text-muted-foreground'
              )}
            >
              Grid
            </button>
            <button
              onClick={() => setView('flow')}
              className={cn(
                "px-3 py-1.5 rounded-md text-sm transition-colors",
                view === 'flow' ? 'bg-primary text-primary-foreground' : 'text-muted-foreground'
              )}
            >
              Flow
            </button>
          </div>
          <button className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors">
            <Plus className="w-4 h-4" />
            New Workflow
          </button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-4 gap-4">
        <div className="p-4 bg-card rounded-xl border border-border">
          <p className="text-3xl font-bold">24</p>
          <p className="text-sm text-muted-foreground">Total Workflows</p>
        </div>
        <div className="p-4 bg-card rounded-xl border border-border">
          <p className="text-3xl font-bold text-blue-500">5</p>
          <p className="text-sm text-muted-foreground">Running</p>
        </div>
        <div className="p-4 bg-card rounded-xl border border-border">
          <p className="text-3xl font-bold text-green-500">142</p>
          <p className="text-sm text-muted-foreground">Completed Today</p>
        </div>
        <div className="p-4 bg-card rounded-xl border border-border">
          <p className="text-3xl font-bold text-yellow-500">87%</p>
          <p className="text-sm text-muted-foreground">Success Rate</p>
        </div>
      </div>

      {view === 'grid' ? (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {SAMPLE_WORKFLOWS.map(workflow => (
            <WorkflowCard key={workflow.id} workflow={workflow} />
          ))}
        </div>
      ) : (
        <div className="p-8 bg-card rounded-xl border border-border min-h-[500px] flex items-center justify-center">
          <div className="text-center">
            <GitBranch className="w-16 h-16 mx-auto text-muted-foreground mb-4" />
            <p className="text-muted-foreground">Visual workflow editor coming soon</p>
          </div>
        </div>
      )}
    </div>
  );
}
