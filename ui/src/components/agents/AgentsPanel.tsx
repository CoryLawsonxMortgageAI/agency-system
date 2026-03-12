import { useState } from 'react';
import { useApi } from '@/hooks/useApi';
import { AgentConfig, AgentStatus, DIVISION_COLORS } from '@/types';
import { 
  Bot, 
  Search, 
  Filter, 
  Play, 
  MoreVertical,
  Brain,
  Code,
  Palette,
  Shield,
  Sparkles,
  Zap,
  Users
} from 'lucide-react';
import { cn } from '@/lib/utils';

const DIVISION_ICONS: Record<string, React.ElementType> = {
  Engineering: Code,
  Marketing: Palette,
  Product: Brain,
  Testing: Shield,
  Support: Users,
  Specialized: Sparkles,
};

function AgentCard({ agent, status }: { agent: AgentConfig; status?: AgentStatus }) {
  const [isHovered, setIsHovered] = useState(false);
  const DivisionIcon = DIVISION_ICONS[agent.division] || Bot;
  
  const isActive = status?.status === 'active' || status?.status === 'idle';
  
  return (
    <div 
      className={cn(
        "group relative p-5 rounded-xl border transition-all duration-300",
        "bg-card hover:bg-accent/50",
        isActive ? "border-green-500/30" : "border-border",
        isActive && "shadow-lg shadow-green-500/5"
      )}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Status Indicator */}
      <div className={cn(
        "absolute top-4 right-4 w-3 h-3 rounded-full",
        isActive ? "bg-green-500 animate-pulse" : "bg-gray-500"
      )} />
      
      {/* Header */}
      <div className="flex items-start gap-4">
        <div className={cn(
          "p-3 rounded-xl transition-transform duration-300",
          DIVISION_COLORS[agent.division] || 'bg-gray-500',
          isHovered && "scale-110"
        )}>
          <DivisionIcon className="w-6 h-6" />
        </div>
        
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-lg truncate">{agent.name}</h3>
          <p className="text-sm text-muted-foreground">{agent.personality.role}</p>
          <div className="flex items-center gap-2 mt-2">
            <span className={cn(
              "text-xs px-2 py-0.5 rounded-full",
              DIVISION_COLORS[agent.division] || 'bg-gray-500'
            )}>
              {agent.division}
            </span>
            <span className="text-xs text-muted-foreground">{agent.model}</span>
          </div>
        </div>
      </div>
      
      {/* Catchphrase */}
      {agent.personality.catchphrase && (
        <p className="mt-4 text-sm italic text-muted-foreground border-l-2 border-primary/30 pl-3">
          "{agent.personality.catchphrase}"
        </p>
      )}
      
      {/* Capabilities */}
      <div className="mt-4">
        <p className="text-xs text-muted-foreground mb-2">Expertise</p>
        <div className="flex flex-wrap gap-1">
          {agent.personality.expertise_areas.slice(0, 4).map((skill) => (
            <span key={skill} className="text-xs bg-accent px-2 py-1 rounded">
              {skill}
            </span>
          ))}
        </div>
      </div>
      
      {/* Status Bar */}
      {status && (
        <div className="mt-4 pt-4 border-t border-border">
          <div className="flex items-center justify-between text-xs">
            <div className="flex items-center gap-4">
              <span className="text-muted-foreground">
                Tasks: <span className="text-foreground">{status.total_tasks_completed}</span>
              </span>
              <span className="text-muted-foreground">
                Queue: <span className="text-foreground">{status.queue_depth}</span>
              </span>
            </div>
            <span className={cn(
              "capitalize",
              status.status === 'busy' ? 'text-yellow-500' : 
              status.status === 'error' ? 'text-red-500' : 'text-green-500'
            )}>
              {status.status}
            </span>
          </div>
        </div>
      )}
      
      {/* Actions */}
      <div className={cn(
        "mt-4 flex gap-2 transition-opacity duration-200",
        isHovered ? "opacity-100" : "opacity-0"
      )}>
        <button className="flex-1 flex items-center justify-center gap-2 px-3 py-2 bg-primary text-primary-foreground rounded-lg text-sm hover:bg-primary/90 transition-colors">
          <Play className="w-4 h-4" />
          Execute
        </button>
        <button className="p-2 hover:bg-accent rounded-lg transition-colors">
          <MoreVertical className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}

export function AgentsPanel() {
  const { data: agents } = useApi<AgentConfig[]>('/agents', 10000);
  const [selectedDivision, setSelectedDivision] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState('');

  const divisions = ['all', 'Engineering', 'Marketing', 'Product', 'Testing', 'Support', 'Specialized'];
  
  const filteredAgents = agents?.filter(agent => {
    const matchesDivision = selectedDivision === 'all' || agent.division === selectedDivision;
    const matchesSearch = agent.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         agent.personality.role.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesDivision && matchesSearch;
  });

  const stats = {
    total: agents?.length || 0,
    active: agents?.filter(a => a.active).length || 0,
    engineering: agents?.filter(a => a.division === 'Engineering').length || 0,
    marketing: agents?.filter(a => a.division === 'Marketing').length || 0,
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Agent Roster</h2>
          <p className="text-muted-foreground">Manage and deploy your AI agent swarm</p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors">
          <Sparkles className="w-4 h-4" />
          Deploy Agent
        </button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-4 gap-4">
        <div className="p-4 bg-card rounded-xl border border-border">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-500/20 rounded-lg">
              <Bot className="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.total}</p>
              <p className="text-xs text-muted-foreground">Total Agents</p>
            </div>
          </div>
        </div>
        <div className="p-4 bg-card rounded-xl border border-border">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-green-500/20 rounded-lg">
              <Zap className="w-5 h-5 text-green-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.active}</p>
              <p className="text-xs text-muted-foreground">Active</p>
            </div>
          </div>
        </div>
        <div className="p-4 bg-card rounded-xl border border-border">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-purple-500/20 rounded-lg">
              <Code className="w-5 h-5 text-purple-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.engineering}</p>
              <p className="text-xs text-muted-foreground">Engineering</p>
            </div>
          </div>
        </div>
        <div className="p-4 bg-card rounded-xl border border-border">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-pink-500/20 rounded-lg">
              <Palette className="w-5 h-5 text-pink-500" />
            </div>
            <div>
              <p className="text-2xl font-bold">{stats.marketing}</p>
              <p className="text-xs text-muted-foreground">Marketing</p>
            </div>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="flex items-center gap-4">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search agents..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-card border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
          />
        </div>
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-muted-foreground" />
          {divisions.map(division => (
            <button
              key={division}
              onClick={() => setSelectedDivision(division)}
              className={cn(
                "px-3 py-1.5 rounded-lg text-sm transition-colors",
                selectedDivision === division
                  ? "bg-primary text-primary-foreground"
                  : "bg-card border border-border hover:bg-accent"
              )}
            >
              {division.charAt(0).toUpperCase() + division.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Agents Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredAgents?.map(agent => (
          <AgentCard key={agent.id} agent={agent} />
        ))}
      </div>
    </div>
  );
}
