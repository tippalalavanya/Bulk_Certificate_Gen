'use client'

import { useCallback, useEffect, useMemo, useState } from 'react'
import {
  ArrowUpRight,
  Award,
  Check,
  ChevronRight,
  CircleAlert,
  Clock3,
  Download,
  FileCheck2,
  Loader2,
  Plus,
  RefreshCw,
  Send,
  ShieldCheck,
  Trash2,
  Users,
  X,
} from 'lucide-react'

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'

type Recipient = { name: string; email: string }
type Job = {
  job_id: string
  status: string
  total_count: number
  successful_count: number
  failed_count: number
  pending_count: number
  processing_count: number
  progress_percentage: number
  created_at: string
  completed_at?: string | null
}
type Result = { result_id: string; name: string; status: string; certificate_id?: string | null; failure_message?: string | null }

const initialRecipients: Recipient[] = [{ name: '', email: '' }]

export default function Page() {
  const [course, setCourse] = useState('Python Backend Development')
  const [issueDate, setIssueDate] = useState('2026-10-10')
  const [recipients, setRecipients] = useState<Recipient[]>(initialRecipients)
  const [job, setJob] = useState<Job | null>(null)
  const [results, setResults] = useState<Result[]>([])
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [notice, setNotice] = useState<{ type: 'error' | 'success'; text: string } | null>(null)

  const completed = job?.successful_count ?? 0
  const failed = job?.failed_count ?? 0
  const pending = (job?.pending_count ?? 0) + (job?.processing_count ?? 0)
  const isActive = Boolean(job && ['queued', 'processing'].includes(job.status))

  const loadJob = useCallback(async (jobId: string) => {
    try {
      const response = await fetch(`${API_BASE}/api/v1/certificate-jobs/${jobId}`, { cache: 'no-store' })
      if (!response.ok) return
      const nextJob: Job = await response.json()
      setJob(nextJob)
      const resultsResponse = await fetch(`${API_BASE}/api/v1/certificate-jobs/${jobId}/results`, { cache: 'no-store' })
      if (resultsResponse.ok) setResults((await resultsResponse.json()).items)
    } catch {
      // The dashboard remains usable if the local API is temporarily offline.
    }
  }, [])

  useEffect(() => {
    if (!job || !isActive) return
    const timer = window.setInterval(() => void loadJob(job.job_id), 1200)
    return () => window.clearInterval(timer)
  }, [job, isActive, loadJob])

  function updateRecipient(index: number, field: keyof Recipient, value: string) {
    setRecipients((current) => current.map((recipient, itemIndex) => itemIndex === index ? { ...recipient, [field]: value } : recipient))
  }

  function addRecipient() { setRecipients((current) => [...current, { name: '', email: '' }]) }
  function removeRecipient(index: number) { setRecipients((current) => current.length === 1 ? current : current.filter((_, itemIndex) => itemIndex !== index)) }

  async function createJob(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setNotice(null)
    setIsSubmitting(true)
    try {
      const response = await fetch(`${API_BASE}/api/v1/certificate-jobs`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ coursename: course, issuedate: issueDate, recipients }),
      })
      const body = await response.json().catch(() => null)
      if (!response.ok) throw new Error(body?.detail?.message ?? 'Unable to create certificate job.')
      setJob(body)
      setResults([])
      setNotice({ type: 'success', text: 'Job accepted. Certificates are being generated.' })
    } catch (error) {
      setNotice({ type: 'error', text: error instanceof Error ? error.message : 'Unable to reach the certificate API.' })
    } finally { setIsSubmitting(false) }
  }

  const statusLabel = job?.status?.replaceAll('_', ' ') ?? 'Ready to generate'
  const progress = Math.round(job?.progress_percentage ?? 0)

  return (
    <main className="min-h-screen bg-[#f7f8fa] text-[#152033] dark:bg-[#0c111b] dark:text-[#f4f7fb]">
      <header className="border-b border-[#e7ebf0] bg-white/90 dark:border-white/10 dark:bg-[#101722]/90">
        <div className="mx-auto flex max-w-[1360px] items-center justify-between px-5 py-4 lg:px-8">
          <div className="flex items-center gap-3">
            <div className="flex size-10 items-center justify-center rounded-xl bg-[#102a43] text-[#8ee3c7] shadow-sm"><Award className="size-5" /></div>
            <div><p className="text-sm font-semibold tracking-tight">Certify</p><p className="text-[11px] text-[#718096]">Bulk certificate operations</p></div>
          </div>
          <div className="hidden items-center gap-6 text-xs font-medium text-[#718096] md:flex"><span className="flex items-center gap-2"><span className="size-2 rounded-full bg-[#31b77a]" /> API online</span><span>v1.0.0</span></div>
        </div>
      </header>

      <div className="mx-auto grid max-w-[1360px] gap-8 px-5 py-8 lg:grid-cols-[minmax(0,1fr)_360px] lg:px-8 lg:py-10">
        <section>
          <div className="mb-8"><p className="mb-2 text-xs font-semibold uppercase tracking-[0.2em] text-[#158f78]">Certificate studio</p><h1 className="text-3xl font-semibold tracking-[-0.04em] sm:text-4xl">Create a certificate batch</h1><p className="mt-3 max-w-xl text-sm leading-6 text-[#718096]">Personalize and generate secure PDF certificates for your recipients in one streamlined job.</p></div>
          <form onSubmit={createJob} className="space-y-5">
            <div className="rounded-2xl border border-[#e1e7ed] bg-white p-5 shadow-[0_8px_30px_rgba(30,52,73,0.04)] dark:border-white/10 dark:bg-[#111a27] sm:p-6">
              <div className="mb-5 flex items-center justify-between"><div><h2 className="text-sm font-semibold">Certificate details</h2><p className="mt-1 text-xs text-[#718096]">Shared across every certificate in this batch.</p></div><FileCheck2 className="size-5 text-[#158f78]" /></div>
              <div className="grid gap-4 sm:grid-cols-[1fr_190px]"><label className="space-y-2 text-xs font-semibold">Course or event name<input required value={course} onChange={(event) => setCourse(event.target.value)} className="field" placeholder="e.g. Advanced Python" /></label><label className="space-y-2 text-xs font-semibold">Issue date<input required type="date" value={issueDate} onChange={(event) => setIssueDate(event.target.value)} className="field" /></label></div>
            </div>
            <div className="rounded-2xl border border-[#e1e7ed] bg-white p-5 shadow-[0_8px_30px_rgba(30,52,73,0.04)] dark:border-white/10 dark:bg-[#111a27] sm:p-6">
              <div className="mb-5 flex items-center justify-between"><div><h2 className="text-sm font-semibold">Recipients <span className="ml-1 rounded-full bg-[#edf8f5] px-2 py-0.5 text-[11px] text-[#158f78] dark:bg-[#123b36]">{recipients.length}</span></h2><p className="mt-1 text-xs text-[#718096]">Add each person who should receive a certificate.</p></div><Users className="size-5 text-[#8a96a8]" /></div>
              <div className="space-y-3">{recipients.map((recipient, index) => <div key={index} className="grid gap-3 rounded-xl border border-[#edf0f3] bg-[#fbfcfd] p-3 dark:border-white/10 dark:bg-white/[0.025] sm:grid-cols-[1fr_1fr_36px]"><label className="sr-only" htmlFor={`name-${index}`}>Recipient name</label><input id={`name-${index}`} required value={recipient.name} onChange={(event) => updateRecipient(index, 'name', event.target.value)} className="field field-compact" placeholder="Full name" /><label className="sr-only" htmlFor={`email-${index}`}>Recipient email</label><input id={`email-${index}`} required type="email" value={recipient.email} onChange={(event) => updateRecipient(index, 'email', event.target.value)} className="field field-compact" placeholder="Email address" /><button type="button" onClick={() => removeRecipient(index)} disabled={recipients.length === 1} className="icon-button" aria-label={`Remove recipient ${index + 1}`}><Trash2 className="size-4" /></button></div>)}</div>
              <button type="button" onClick={addRecipient} className="mt-4 inline-flex items-center gap-2 text-xs font-semibold text-[#158f78] transition hover:text-[#0c705f]"><Plus className="size-4" /> Add recipient</button>
            </div>
            {notice && <div role="alert" className={`flex items-start gap-3 rounded-xl border px-4 py-3 text-sm ${notice.type === 'error' ? 'border-[#f5caca] bg-[#fff6f6] text-[#b33b3b]' : 'border-[#bfe8dc] bg-[#f0fbf7] text-[#13745f]'}`}>{notice.type === 'error' ? <CircleAlert className="mt-0.5 size-4 shrink-0" /> : <Check className="mt-0.5 size-4 shrink-0" />}{notice.text}</div>}
            <div className="flex flex-col items-start justify-between gap-3 sm:flex-row sm:items-center"><p className="flex items-center gap-2 text-xs text-[#718096]"><ShieldCheck className="size-4 text-[#158f78]" /> PDFs are stored outside public static files.</p><button disabled={isSubmitting} className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-[#102a43] px-5 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-[#193d5c] disabled:cursor-not-allowed disabled:opacity-60 sm:w-auto">{isSubmitting ? <Loader2 className="size-4 animate-spin" /> : <Send className="size-4" />}{isSubmitting ? 'Submitting…' : 'Generate certificates'}<ArrowUpRight className="size-4 opacity-60" /></button></div>
          </form>
        </section>

        <aside className="space-y-5">
          <div className="rounded-2xl border border-[#e1e7ed] bg-[#102a43] p-5 text-white shadow-[0_12px_35px_rgba(16,42,67,0.16)] sm:p-6"><div className="flex items-start justify-between"><div><p className="text-xs font-semibold uppercase tracking-[0.16em] text-[#8ee3c7]">Live job monitor</p><h2 className="mt-2 text-xl font-semibold">{job ? statusLabel : 'No active job'}</h2></div><div className="rounded-lg bg-white/10 p-2">{isActive ? <Loader2 className="size-5 animate-spin text-[#8ee3c7]" /> : <Clock3 className="size-5 text-[#8ee3c7]" />}</div></div><div className="mt-7"><div className="mb-2 flex justify-between text-xs text-white/65"><span>Progress</span><span className="font-semibold text-white">{progress}%</span></div><div className="h-2 overflow-hidden rounded-full bg-white/15"><div className="h-full rounded-full bg-[#8ee3c7] transition-all duration-500" style={{ width: `${progress}%` }} /></div></div><div className="mt-6 grid grid-cols-3 gap-2 border-t border-white/10 pt-5 text-center"><div><p className="text-xl font-semibold">{completed}</p><p className="mt-1 text-[10px] uppercase tracking-wider text-white/55">Done</p></div><div><p className="text-xl font-semibold">{pending}</p><p className="mt-1 text-[10px] uppercase tracking-wider text-white/55">Pending</p></div><div><p className="text-xl font-semibold">{failed}</p><p className="mt-1 text-[10px] uppercase tracking-wider text-white/55">Failed</p></div></div></div>
          <div className="rounded-2xl border border-[#e1e7ed] bg-white p-5 dark:border-white/10 dark:bg-[#111a27] sm:p-6"><div className="flex items-center justify-between"><h2 className="text-sm font-semibold">Batch results</h2>{job && <button type="button" onClick={() => void loadJob(job.job_id)} className="icon-button" aria-label="Refresh results"><RefreshCw className="size-4" /></button>}</div>{job ? <><p className="mt-1 truncate font-mono text-[10px] text-[#8a96a8]">{job.job_id}</p><div className="mt-4 space-y-2">{results.length ? results.map((result) => <div key={result.result_id} className="flex items-center justify-between rounded-lg border border-[#edf0f3] px-3 py-2.5 dark:border-white/10"><div className="min-w-0"><p className="truncate text-xs font-medium">{result.name}</p><p className={`mt-0.5 text-[10px] capitalize ${result.status === 'completed' ? 'text-[#158f78]' : result.status === 'failed' ? 'text-[#b33b3b]' : 'text-[#8a96a8]'}`}>{result.status}</p></div>{result.certificate_id && <a href={`${API_BASE}/api/v1/certificates/${result.certificate_id}`} target="_blank" rel="noreferrer" className="ml-3 rounded-md p-1.5 text-[#158f78] transition hover:bg-[#edf8f5]" aria-label={`Download certificate for ${result.name}`}><Download className="size-4" /></a>}</div>) : <div className="py-7 text-center text-xs text-[#8a96a8]">Results will appear as recipients finish.</div>}</div></> : <div className="py-8 text-center"><div className="mx-auto mb-3 flex size-10 items-center justify-center rounded-full bg-[#f1f4f7] text-[#8a96a8] dark:bg-white/10"><FileCheck2 className="size-5" /></div><p className="text-xs text-[#718096]">Submit a batch to track it here.</p></div>}</div>
          <div className="rounded-2xl border border-[#d8eee7] bg-[#f0fbf7] p-4 text-xs leading-5 text-[#246b5c] dark:border-[#1e5148] dark:bg-[#102a35] dark:text-[#a7e0d0]"><p className="font-semibold">How processing works</p><p className="mt-1">Each recipient is processed independently. One failure will not stop the remaining certificates from being generated.</p></div>
        </aside>
      </div>
      <footer className="mx-auto flex max-w-[1360px] items-center gap-2 px-5 pb-8 text-[11px] text-[#8a96a8] lg:px-8"><span>Certificate generation API</span><ChevronRight className="size-3" /><span>Local workspace</span></footer>
    </main>
  )
}

// Shared form styles keep the dense workflow readable on small screens.
const _styles = ''
