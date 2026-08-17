import { useMemo } from 'react'
import {
  Background,
  Controls,
  Handle,
  MarkerType,
  MiniMap,
  Position,
  ReactFlow,
} from '@xyflow/react'
import YAML from 'yaml'
import '@xyflow/react/dist/style.css'
import './App.css'
import storyYaml from '../../terma/assets/stories/gemini_story.yaml?raw'

const NODE_ID_PATTERN = /^\d+$/
const COLUMN_GAP = 560
const ROW_GAP = 320

function shortenText(value, limit = 180) {
  const compact = String(value ?? '').replace(/\s+/g, ' ').trim()

  if (!compact) {
    return 'No text provided.'
  }

  return compact.length > limit ? `${compact.slice(0, limit).trim()}…` : compact
}

function parseStory(rawStory) {
  const parsed = YAML.parse(rawStory)
  const source = parsed && typeof parsed === 'object' ? parsed : {}
  const metadata = source.metadata ?? source.metdata ?? {}
  const storyNodes = Object.entries(source)
    .filter(([key, value]) => NODE_ID_PATTERN.test(key) && value && typeof value === 'object')
    .map(([key, value]) => {
      const choices = Array.isArray(value.choices)
        ? value.choices.map((choice, index) => ({
            index,
            text: String(choice?.text ?? `Choice ${index + 1}`),
            rawTarget: choice?.next_node,
            nextNode:
              typeof choice?.next_node === 'number'
                ? choice.next_node
                : Number.parseInt(choice?.next_node, 10),
          }))
        : []

      return {
        id: Number.parseInt(key, 10),
        location: String(value.location ?? `Node ${key}`),
        text: String(value.text ?? ''),
        choices,
      }
    })
    .sort((left, right) => left.id - right.id)

  const nodesById = new Map(storyNodes.map((node) => [node.id, node]))
  const rootNode = storyNodes[0]
  const depthByNodeId = new Map()

  if (rootNode) {
    const queue = [rootNode.id]
    depthByNodeId.set(rootNode.id, 0)

    while (queue.length > 0) {
      const currentId = queue.shift()
      const currentNode = nodesById.get(currentId)

      if (!currentNode) {
        continue
      }

      const currentDepth = depthByNodeId.get(currentId) ?? 0

      for (const choice of currentNode.choices) {
        if (!Number.isInteger(choice.nextNode) || !nodesById.has(choice.nextNode)) {
          continue
        }

        if (!depthByNodeId.has(choice.nextNode)) {
          depthByNodeId.set(choice.nextNode, currentDepth + 1)
          queue.push(choice.nextNode)
        }
      }
    }
  }

  const reachableIds = new Set(depthByNodeId.keys())
  const depthValues = [...depthByNodeId.values()]
  const deepestReachable = depthValues.length > 0 ? Math.max(...depthValues) : 0
  const unreachableNodes = storyNodes.filter((node) => !reachableIds.has(node.id))

  unreachableNodes.forEach((node, index) => {
    depthByNodeId.set(node.id, deepestReachable + 1 + Math.floor(index / 2))
  })

  const columns = new Map()
  for (const node of storyNodes) {
    const depth = depthByNodeId.get(node.id) ?? 0
    const column = columns.get(depth) ?? []
    column.push(node)
    columns.set(depth, column)
  }

  const incomingCounts = new Map(storyNodes.map((node) => [node.id, 0]))
  const edges = []
  const danglingChoices = []

  for (const node of storyNodes) {
    for (const choice of node.choices) {
      if (!Number.isInteger(choice.nextNode) || !nodesById.has(choice.nextNode)) {
        danglingChoices.push({ from: node.id, choice: choice.text, target: choice.rawTarget })
        continue
      }

      incomingCounts.set(choice.nextNode, (incomingCounts.get(choice.nextNode) ?? 0) + 1)

      edges.push({
        id: `${node.id}-${choice.nextNode}-${choice.index}`,
        source: String(node.id),
        target: String(choice.nextNode),
        label: choice.text,
        labelStyle: {
          fill: '#f8e9c0',
          fontSize: 11,
          fontWeight: 600,
        },
        labelBgStyle: {
          fill: 'rgba(13, 17, 28, 0.94)',
          color: '#f8e9c0',
        },
        labelBgPadding: [8, 5],
        labelBgBorderRadius: 999,
        style: {
          stroke: choice.nextNode === node.id ? '#f59e0b' : '#d97706',
          strokeWidth: choice.nextNode === node.id ? 2.5 : 1.7,
        },
        markerEnd: {
          type: MarkerType.ArrowClosed,
          color: choice.nextNode === node.id ? '#f59e0b' : '#d97706',
        },
      })
    }
  }

  const graphNodes = storyNodes.map((node) => {
    const depth = depthByNodeId.get(node.id) ?? 0
    const column = columns.get(depth) ?? []
    const rowIndex = column.findIndex((candidate) => candidate.id === node.id)
    const yOffset = ((column.length - 1) * ROW_GAP) / 2

    return {
      id: String(node.id),
      type: 'story',
      position: {
        x: depth * COLUMN_GAP,
        y: rowIndex * ROW_GAP - yOffset,
      },
      data: {
        id: node.id,
        location: node.location,
        text: node.text,
        textPreview: shortenText(node.text, 220),
        choices: node.choices,
        outgoingCount: node.choices.length,
        incomingCount: incomingCounts.get(node.id) ?? 0,
        isTerminal: node.choices.length === 0,
        isUnreachable: !reachableIds.has(node.id),
        isRoot: node.id === rootNode?.id,
      },
      sourcePosition: Position.Right,
      targetPosition: Position.Left,
    }
  })

  const terminalNodes = storyNodes.filter((node) => node.choices.length === 0)

  return {
    metadata,
    nodes: graphNodes,
    edges,
    rootNode,
    terminalNodes,
    danglingChoices,
    stats: {
      nodeCount: storyNodes.length,
      choiceCount: edges.length,
      terminalCount: terminalNodes.length,
      unreachableCount: unreachableNodes.length,
    },
  }
}

function StoryNode({ data }) {
  return (
    <div
      className={`story-node${data.isRoot ? ' story-node--root' : ''}${data.isTerminal ? ' story-node--terminal' : ''}${data.isUnreachable ? ' story-node--unreachable' : ''}`}
    >
      <Handle type="target" position={Position.Left} />
      <Handle type="source" position={Position.Right} />
      <div className="story-node__topline">
        <span>Node {data.id}</span>
        <span>{data.outgoingCount} choices</span>
      </div>
      <h3>{data.location}</h3>
      <p>{data.textPreview}</p>
      <div className="story-node__footer">
        <span>{data.incomingCount} incoming</span>
        {data.isTerminal ? <span>Terminal</span> : <span>Branching</span>}
      </div>
      {data.choices.length > 0 ? (
        <ul className="story-node__choices">
          {data.choices.slice(0, 3).map((choice) => (
            <li key={`${data.id}-${choice.index}`}>
              <span>{choice.text}</span>
              <strong>{Number.isInteger(choice.nextNode) ? `→ ${choice.nextNode}` : '→ ?'}</strong>
            </li>
          ))}
          {data.choices.length > 3 ? <li className="story-node__choices-more">+ {data.choices.length - 3} more</li> : null}
        </ul>
      ) : null}
    </div>
  )
}

export default function App() {
  const story = useMemo(() => parseStory(storyYaml), [])
  const nodeTypes = useMemo(() => ({ story: StoryNode }), [])

  return (
    <div className="app-shell">
      <header className="hero-panel">
        <div>
          <p className="eyebrow">Story visualization</p>
          <h1>{story.metadata.title ?? 'Gemini Story'}</h1>
          <p className="hero-panel__description">
            {story.metadata.description ?? 'A branching labyrinth story loaded directly from the terma assets folder.'}
          </p>
        </div>
        <div className="hero-panel__meta">
          <div>
            <span>Author</span>
            <strong>{story.metadata.author ?? 'Unknown'}</strong>
          </div>
          <div>
            <span>Version</span>
            <strong>{story.metadata.version ?? 'N/A'}</strong>
          </div>
          <div>
            <span>Created</span>
            <strong>{story.metadata.created ?? 'N/A'}</strong>
          </div>
          <div>
            <span>Tag count</span>
            <strong>{Array.isArray(story.metadata.tags) ? story.metadata.tags.length : 0}</strong>
          </div>
        </div>
      </header>

      <section className="stats-strip">
        <article>
          <span>Nodes</span>
          <strong>{story.stats.nodeCount}</strong>
        </article>
        <article>
          <span>Choices</span>
          <strong>{story.stats.choiceCount}</strong>
        </article>
        <article>
          <span>Endings</span>
          <strong>{story.stats.terminalCount}</strong>
        </article>
        <article>
          <span>Unreachable</span>
          <strong>{story.stats.unreachableCount}</strong>
        </article>
      </section>

      <main className="workspace">
        <section className="flow-panel">
          <div className="flow-panel__header">
            <div>
              <p className="eyebrow">Graph view</p>
              <h2>Branching structure</h2>
            </div>
            <p>
              Edges are derived from each choice&apos;s <code>next_node</code> value and the layout keeps reachable paths on the left-to-right flow.
            </p>
          </div>
          <div className="flow-panel__canvas">
            <ReactFlow
              nodes={story.nodes}
              edges={story.edges}
              nodeTypes={nodeTypes}
              fitView
              fitViewOptions={{ padding: 0.2 }}
              nodesConnectable={false}
              nodesDraggable={false}
              panOnScroll
              zoomOnDoubleClick={false}
            >
              <MiniMap zoomable pannable nodeColor={(node) => (node.data?.isTerminal ? '#7c2d12' : '#1d4ed8')} />
              <Controls />
              <Background color="rgba(251, 191, 36, 0.18)" gap={24} />
            </ReactFlow>
          </div>
        </section>

        <aside className="inspector-panel">
          <section>
            <p className="eyebrow">Story metadata</p>
            <h2>{story.rootNode ? `Start at node ${story.rootNode.id}` : 'No story nodes found'}</h2>
            <div className="inspector-panel__text">
              <p>
                The source story is loaded from <code>terma/assets/stories/gemini_story.yaml</code> and parsed at build time.
              </p>
              <p>
                This view is read-only. The graph is meant to help you inspect branching, loops, endings, and disconnected nodes.
              </p>
            </div>
          </section>

          <section>
            <p className="eyebrow">Terminal nodes</p>
            <ul className="inspector-list">
              {story.terminalNodes.slice(0, 8).map((node) => (
                <li key={node.id}>
                  <strong>{node.id}</strong>
                  <span>{node.location}</span>
                </li>
              ))}
              {story.terminalNodes.length > 8 ? <li className="inspector-list__more">+ {story.terminalNodes.length - 8} more endings</li> : null}
            </ul>
          </section>

          {story.danglingChoices.length > 0 ? (
            <section>
              <p className="eyebrow">Broken references</p>
              <ul className="inspector-list inspector-list--warning">
                {story.danglingChoices.slice(0, 5).map((entry, index) => (
                  <li key={`${entry.from}-${index}`}>
                    <strong>{entry.from}</strong>
                    <span>{entry.choice}</span>
                  </li>
                ))}
                {story.danglingChoices.length > 5 ? <li className="inspector-list__more">+ {story.danglingChoices.length - 5} more</li> : null}
              </ul>
            </section>
          ) : null}
        </aside>
      </main>
    </div>
  )
}