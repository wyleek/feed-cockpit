import Anthropic from '@anthropic-ai/sdk';
import { readFileSync, existsSync, readdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..', '..');

function read(path) {
  return existsSync(path) ? readFileSync(path, 'utf-8') : '';
}

export default async function handler(req) {
  if (req.method !== 'POST') {
    return new Response('Method not allowed', { status: 405 });
  }

  if (!process.env.ANTHROPIC_API_KEY) {
    return Response.json({
      ok: false,
      error: 'ANTHROPIC_API_KEY not configured — add it in Netlify → Site settings → Environment variables',
    }, { status: 500 });
  }

  let story, component;
  try {
    ({ story, component = 'script' } = await req.json());
  } catch {
    return Response.json({ ok: false, error: 'Invalid request body' }, { status: 400 });
  }

  const packDir = join(ROOT, 'content-engine', 'packs', 'wellness-genz');
  const voiceDir = join(packDir, 'voice');
  const fmtDir = join(packDir, 'formats');

  const parts = [
    'You are a short-form video content writer for a Gen Z wellness channel.',
    'PACK CONTEXT:\n' + read(join(packDir, 'pack.md')),
    'VOICE BIBLE:\n' + read(join(voiceDir, 'voice-bible.md')),
    'VIDEO SCRIPT FORMAT:\n' + read(join(fmtDir, 'video-script.md')),
  ];

  if (['captions', 'package'].includes(component)) {
    parts.push('CAPTIONS FORMAT:\n' + read(join(fmtDir, 'captions.md')));
  }

  const examplesDir = join(voiceDir, 'examples');
  if (existsSync(examplesDir)) {
    const examples = readdirSync(examplesDir)
      .filter(f => f.endsWith('.md'))
      .slice(0, 2)
      .map(f => readFileSync(join(examplesDir, f), 'utf-8'));
    if (examples.length) {
      parts.push('GOLD EXAMPLES (imitate their rhythm):\n' + examples.join('\n\n---\n\n'));
    }
  }

  parts.push('Generate ONLY the requested component. No preamble, no commentary — deliver the output directly.');
  const system = parts.filter(Boolean).join('\n\n');

  const srcs = story.sources || [];
  const userMsg = [
    `Generate a ${component} for this story.`,
    '',
    `Headline: ${story.headline || ''}`,
    `Summary: ${story.summary || ''}`,
    `Source: ${srcs[0]?.outlet || 'Unknown'}`,
    `URL: ${srcs[0]?.url || ''}`,
    `Keywords: ${(story.keyword_hits || []).join(', ')}`,
  ].join('\n');

  try {
    const client = new Anthropic();
    const message = await client.messages.create({
      model: 'claude-sonnet-4-6',
      max_tokens: 1500,
      system,
      messages: [{ role: 'user', content: userMsg }],
    });
    return Response.json({ ok: true, content: message.content[0].text, component });
  } catch (e) {
    return Response.json({ ok: false, error: e.message }, { status: 500 });
  }
}

export const config = { path: '/generate' };
