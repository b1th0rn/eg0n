import { api } from '../utils.js'


export function attributeCrud() {
    return {
        // 🔹 STATE
        loading: false, // Track requests
        attribute_type: 'vuln', // Default option
        attribute_data: {
            codesnippet: {
                code: '',
                confidence: '',
                description: '',
                language: '',
                name: '', // URL ?
                // validation_status: '', // Missing?
            },
            fqdn: {
                confidence: '',
                description: '',
                fqdn: '',
                ip_address: '', // ?
                validation_status: '',
            },
            hash: {
                confidence: '',
                description: '',
                filename: '',
                md5: '',
                platform: '',
                sha1: '',
                sha256: '',
                validation_status: '',
                website: '', // -> URL
            },
            ipadd: {
                confidence: '',
                description: '',
                fqdn: '', // ?
                ip_address: '',
                url: '', // ?
                validation_status: '',
            },
            vuln: {
                cve: '',
                cvss: '',
                description: '',
                name: '', // ?
            },
        },

        // 🔹 Attribute CRUD
        async create() {
            if (this.loading) return
            this.loading = true
            console.log('➕ Create a new attribute')
            const url = `/${this.attribute_type}/`
            const payload = this.attribute_data[this.attribute_type]
            const event_pk = this.$root.dataset.event_pk
            payload.event_id = parseInt(event_pk, 10)
            const response = await api.post(url, payload)
            // TODO: must handle response and add a toast
            this.loading = false
        },
        // async read() {
        //     if (this.loading) return
        //     this.loading = true
        //     const pk = this.$el.closest('[data-pk]').dataset.pk
        //     console.log('📖 Read attribute with pk =', pk)
        //     this.loading = false
        // },
        // async update() {
        //     if (this.loading) return
        //     this.loading = true
        //     const pk = this.$el.closest('[data-pk]').dataset.pk
        //     console.log('📝 Update attribute with pk =', pk)
        //     this.loading = false
        // },
        // async delete() {
        //     if (this.loading) return
        //     this.loading = true
        //     const pk = this.$el.closest('[data-pk]').dataset.pk
        //     console.log('🗑️ Delete attribute with pk =', pk)
        //     this.loading = false
        // },

        // 🔹 CVE CRUD
        async readCve() {
            if (this.loading) return
            this.loading = true
            if (this.vuln.cve == "") {
                // CVE field is empty
                console.error('❌ CVE field is empty')
                this.loading = false
                return
            }
            console.log('📖 Read CVE with pk =', this.vuln.cve)
            const response = await api.get(`https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=${this.vuln.cve}`)
            if (response.status === 'success') {
                
                if (response.data.vulnerabilities.length != 1) {
                    console.error(`❌ CVE ${this.vuln.cve} returns zero or multiple hits`)
                } else {
                    console.info(`✅ CVE ${this.vuln.cve} found`)
                    const cve_data = response.data.vulnerabilities[0].cve

                    // Parse language
                    let cve_description = ''
                    if (Array.isArray(cve_data.descriptions)) {
                        const desc = cve_data.descriptions.find(d => d.lang === 'en')
                        if (desc) cve_description = desc.value
                    }

                    // Parse CVSS
                    let cvss = null
                    let cvss_version = null
                    if (cve_data.metrics && typeof cve_data.metrics === 'object') {
                        const metricKeys = Object.keys(cve_data.metrics);
                        for (const key of metricKeys) {
                            const metricArray = cve_data.metrics[key];
                            if (Array.isArray(metricArray) && metricArray.length > 0) {
                                const firstMetric = metricArray[0];
                                if (firstMetric.cvssData && typeof firstMetric.cvssData.baseScore !== 'undefined') {
                                    cvss = firstMetric.cvssData.baseScore;
                                    cvss_version = key; // salva il tipo di metrica
                                    console.log(`✅ Found CVSS ${cvss_version}`)
                                    break
                                }
                            }
                        }
                    }
                    if (!cvss) console.log('⚠️ CVSS not found')

                    // Fill values
                    if (!this.vuln.name || this.vuln.name === "") this.vuln.name = cve_data.id
                    if (!this.vuln.description || this.vuln.description === "") this.vuln.description = cve_description
                    this.vuln.cvss = cvss
                }
            } else {
                console.error('❌ CVE error')
            }            
            this.loading = false
        },
    }
}
