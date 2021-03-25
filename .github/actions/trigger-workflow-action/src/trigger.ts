import * as core from '@actions/core'
import * as github from '@actions/github'
async function run(): Promise<void> {
    try {
        const token = core.getInput('token')
        const workflow = core.getInput('workflow')
        const [ref, owner, repo] = [github.context.ref, github.context.repo.owner, github.context.repo.repo]
        const octokit = github.getOctokit(token)

        const dispatchResp = await octokit.request(`POST /repos/${owner}/${repo}/actions/workflows/${workflow}.yml/dispatches`, {
            ref: ref
        })
        core.info(`API response status: ${dispatchResp.status} 🚀`)
    } catch (error) {
        core.setFailed(error.message)
    }
}

run()