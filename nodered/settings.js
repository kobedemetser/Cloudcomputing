module.exports = {
    uiPort: process.env.PORT || 1880,
    credentialSecret: false,
    flowFile: 'flows.json',
    userDir: '/data',
    functionGlobalContext: {},
    logging: {
        console: {
            level: 'info',
            metrics: false,
            audit: false
        }
    },
    editorTheme: {
        projects: {
            enabled: false
        }
    }
}
