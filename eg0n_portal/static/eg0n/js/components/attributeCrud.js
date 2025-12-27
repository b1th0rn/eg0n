// components/attributeCrud.js
import { api } from '../utils.js'


export function attributeCrud() {
    return {
        // 🔹 HELPERS
        getDefaultExpire() {
            // Today + 30 days
            const d = new Date()
            d.setDate(d.getDate() + 30)
            return d.toISOString().split('T')[0]  // YYYY-MM-DD
        },
        initExpirationDefaults() {
            // Init expire_at when attribute_type changes
            const def = this.getDefaultExpire()
            if (this.attribute_data[this.attribute_type] && "expired_at" in this.attribute_data[this.attribute_type]) {
                this.attribute_data[this.attribute_type].expired_at = def
            }
        },

        // 🔹 STATE
        loading: false, // Track requests
        attribute_type: '', // Default option
        attribute_data: {
            codesnippet: {
                code: '',
                confidence: '',
                description: '',
                language: '',
                name: '',
                expired_at: '',
            },
            fqdn: {
                confidence: '',
                description: '',
                fqdn: '',
                validation_status: '',
                expired_at: '',
            },
            hash: {
                confidence: '',
                description: '',
                filename: '',
                md5: '',
                platform: '',
                sha1: '',
                sha256: '',
                url: '',
                validation_status: '',
                expired_at: '',
            },
            ipadd: {
                confidence: '',
                description: '',
                ip_address: '',
                validation_status: '',
                expired_at: '',
            },
            vuln: {
                cve: '',
                cvss: '',
                description: '',
                name: '',
            },
        },

        // 🔹 Attribute CRUD
        async createItem() {
            if (this.loading) return
            this.loading = true
            console.log('➕ Create a new attribute')
            const url = `/${this.attribute_type}/`
            const payload = this.attribute_data[this.attribute_type]
            payload.event = this.$root.dataset.event_pk
            const response = await api.post(url, payload)
            if (response.status === 'success') {
                console.info(`✅ Attribute added to event ${payload.event}`)
                Alpine.store('message').createItem("Attribute added.", 25)
                window.location.reload()
            } else {
                console.info(`❌ Error while adding attribute to event ${payload.event}`)
                Alpine.store('message').createItem("Error while adding attribute.", 40)
            }
            this.loading = false
        },
        async deleteItem() { // TODO
            if (this.loading) return
            this.loading = true
            console.log('🗑️ Delete an attribute')
            const attribute_type = this.$el.closest('[data-type]').dataset.type
            const pk = this.$el.closest('[data-pk]').dataset.pk
            const url = `/${attribute_type}/${pk}/`
            const response = await api.delete(url)
            if (response.status === 'success') {
                console.info(`✅ Attribute deleted from event`)
                Alpine.store('message').createItem("Attribute deleted.", 25)
                window.location.reload()
            } else {
                console.info(`❌ Error while deleting attribute from event`)
                Alpine.store('message').createItem("Error while deleting attribute.", 40)
            }
            this.loading = false
        },

        // 🔹 CVE CRUD
        async readCve() {
            if (this.loading) return
            this.loading = true
            if (this.attribute_data.vuln.cve == "") {
                // CVE field is empty
                console.error('❌ CVE field is empty')
                this.loading = false
                return
            }
            console.log('📖 Read CVE with pk =', this.attribute_data.vuln.cve)
            const response = await api.get(`https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=${this.attribute_data.vuln.cve}`)
            if (response.status === 'success') {
                
                if (response.data.vulnerabilities.length != 1) {
                    console.error(`❌ CVE ${this.attribute_data.vuln.cve} returns zero or multiple hits`)
                } else {
                    console.info(`✅ CVE ${this.attribute_data.vuln.cve} found`)
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
                                    Alpine.store('message').createItem(`Found CVSS ${cvss_version}`, 25)
                                    break
                                }
                            }
                        }
                    }
                    if (!cvss) {
                        console.log('❌ CVSS format error')
                        Alpine.store('message').createItem("CVSS format error.", 40)
                    }

                    // Fill values
                    if (!this.attribute_data.vuln.name || this.attribute_data.vuln.name === "") this.attribute_data.vuln.name = cve_data.id
                    if (!this.attribute_data.vuln.description || this.attribute_data.vuln.description === "") this.attribute_data.vuln.description = cve_description
                    this.attribute_data.vuln.cvss = cvss
                }
            } else if (response.http.code == 404) {
                console.log('⚠️ CVSS not found')
                Alpine.store('message').createItem("CVSS not found.", 30)
            } else {
                console.error('❌ CVE download error')
                Alpine.store('message').createItem("CVE download error", 40)
            }            
            this.loading = false
        },
    }
}
